from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, mixins, serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from referral_app.models import Users, Referral
from referral_app.serializer import SignupSerializer, ReferralSerializer, UserSerializer
from referral_app.send_email import send_referral_code_email


class UsersViewSet(mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """ Users view set with allowed only retrieve model """

    permission_classes = [AllowAny]
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Get user with requested user id
        :param request: request parameter
        :param args: arguments if any
        :param kwargs: keyword arguments if any
        :return: standard response with success or error
        """
        try:
            user = Users.objects.get(pk=kwargs.get('pk'))
            serializer = UserSerializer(user)
            return Response({
                'status': 'Success',
                'message': "User fetched successfully.",
                'data': serializer.data
            }, 200)
        except ObjectDoesNotExist:
            return Response({
                'status': 'Failed',
                'message': "User not found"
            }, 404)
        except Exception:
            return Response({
                'status': 'Failed',
                'message': 'Error retrieving user.'
            }, 500)


class SignupViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """ Signup viewset with allowed only create model """
    permission_classes = [AllowAny]
    queryset = Users.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        """
        Sign up viewset to create users
        :param request: request parameter
        :param args: arguments if any
        :param kwargs: keyword arguments if any
        :return: standard response with success or error
        """
        try:
            data = request.data
            if data['referral_code'] == '':
                del data['referral_code']
                serializer = SignupSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({
                    'status': 'Success',
                    'message': "Signed up successfully.",
                    'data': serializer.data
                }, 200)
            else:
                referral_code = data['referral_code']
                referrer_user = Users.objects.get(referral_code=referral_code)
                if referrer_user:
                    referrer_obj = Referral.objects.get(referrer=referrer_user, to_email=data['email'])
                    if referrer_obj:
                        serializer = SignupSerializer(data=request.data)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()

                        # Get referred_to user
                        referred_to_user_id = serializer.data['id']
                        referred_user = Users.objects.get(pk=referred_to_user_id)
                        referred_user.points_earned += 100
                        referred_user.save()

                        # Update referrer_user points_earned
                        referrer_user.points_earned += 100
                        referrer_user.save()

                        # Save to Referral model
                        referrer_obj.referred_to = referred_user
                        referrer_obj.status = 'ACCEPTED'
                        referrer_obj.save()
                        return Response({
                            'status': 'Success',
                            'message': "Signed up successfully.",
                            'data': serializer.data
                        }, 200)
                else:
                    serializer = SignupSerializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response({
                        'status': 'Success',
                        'message': "Signed up successfully.",
                        'data': serializer.data
                    }, 200)
        except serializers.ValidationError:
            return Response({
                'status': 'Failed',
                'message': "User with this email already exists."
            }, 400)
        except ObjectDoesNotExist:
            return Response({
                'status': 'Failed',
                'message': "Invalid referral code"
            }, 404)
        except Exception as e:
            return Response({
                'status': 'Failed',
                'message': str(e)
            }, 500)


class ShareReferralCodeViewSet(mixins.CreateModelMixin,
                               viewsets.GenericViewSet):
    """ Share referral code view set with allowed create"""

    permission_classes = [AllowAny]
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer

    def create(self, request, *args, **kwargs):
        """
        Share referral code view set
        :param request: request parameter
        :param args: arguments if any
        :param kwargs: keyword arguments if any
        :return: standard response with success or error
        """
        try:
            data = request.data
            referrer_id, email_to = data['referrer'], data['to_email']
            referrer = Users.objects.get(id=referrer_id)
            serializer = ReferralSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # share referral code to with email
            signup_url = f"{request.build_absolute_uri('/referral/')}signup/"
            send_referral_code_email(email_to, referrer, signup_url)
            return Response({
                'status': 'Success',
                'message': f"Referral code shared with '{email_to}' successfully."
            }, 200)
        except ObjectDoesNotExist:
            return Response({
                'status': 'Failed',
                'message': 'User not found.'
            }, 404)
        except KeyError as e:
            return Response({
                'status': 'Failed',
                'message': f'KeyError: {str(e)}.'
            }, 400)
        except serializers.ValidationError:
            return Response({
                'status': 'Failed',
                'message': "Referral code already shared with email."
            }, 400)
        except Exception:
            return Response({
                'status': 'Failed',
                'message': 'Error sharing referral code.'
            }, 500)
