from rest_framework import status
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action, api_view

from django.views.decorators.csrf import csrf_exempt

from wallet.models import Wallet
from wallet.services import perform_operation
from wallet.api.serializers import WalletOperationSerializer, WalletSerializer


class WalletViewSet(viewsets.ViewSet):
    """
    API endpoint для управления кошельками.
    """

    def list(self, request: Request) -> Response:
        """
        Возвращает список всех кошельков.
        """

        wallets = Wallet.objects.all()
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request: Request, wallet_uuid: str = None) -> Response:
        """
        Возвращает баланс указанного кошелька.

        Args:
            request (Request): Объект запроса.
            wallet_uuid (str): UUID кошелька.
        """

        try:
            wallet = Wallet.objects.get(pk=wallet_uuid)
            return Response({'balance': float(wallet.balance)}, status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({'error': f'Кошелек с UUID {wallet_uuid} не найден.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': f'Неверный формат UUID: {wallet_uuid}.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def info(self, request: Request, wallet_uuid: str = None) -> Response:
        """
        Возвращает данные по кошельку

        Args:
            request (Request): Объект запроса.
            wallet_uuid (str): UUID кошелька.
        """

        try:
            wallet = Wallet.objects.get(pk=wallet_uuid)
            serializer = WalletSerializer(wallet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({'error': f'Кошелек с UUID {wallet_uuid} не найден.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': f'Неверный формат UUID: {wallet_uuid}.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
def operation(request: Request, wallet_uuid: str):
    """
    Обрабатывает POST-запрос для выполнения операций с кошельком (пополнение или списание).

    Args:
        request (Request): Объект запроса, содержащий данные операции.
        wallet_uuid (str): UUID кошелька.
    """

    try:
        serializer = WalletOperationSerializer(data=request.data)

        if serializer.is_valid():
            perform_operation(
                wallet_uuid,
                serializer.validated_data['operation_type'],
                serializer.validated_data['amount']
            )
            return Response({'message': 'Операция выполнена успешно.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Wallet.DoesNotExist:
        return Response({'error': f'Кошелек с UUID {wallet_uuid} не найден.'}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'Внутренняя ошибка сервера: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
