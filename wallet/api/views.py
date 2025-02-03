from typing import Optional

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action

from django.http import Http404
from utilities.logger_utils import logger

from wallet.models import Wallet
from wallet.services import perform_operation
from wallet.api.serializers import WalletOperationSerializer, WalletSerializer


class WalletViewSet(viewsets.ModelViewSet):
    """
    API для управления электронными кошельками.

    Позволяет выполнять следующие операции:
    * Просмотр списка кошельков
    * Получение информации о конкретном кошельке
    * Просмотр баланса
    * Пополнение и снятие средств
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = 'wallet_id'

    @swagger_auto_schema(
        operation_description="Получение списка всех кошельков с их балансами и информацией о владельцах",
        responses={
            200: WalletSerializer(many=True),
            403: "Отказано в доступе. Требуются права администратора."
        },
        tags=['wallets']
    )
    def list(self, request: Request) -> Optional[Response]:
        """
        Возвращает список всех кошельков.
        """

        wallets = self.get_queryset()
        serializer = self.get_serializer(wallets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Получение баланса конкретного кошелька по его UUID",
        responses={
            200: openapi.Response(
                description="Баланс кошелька",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'balance': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description="Текущий баланс кошелька"
                        )
                    }
                )
            ),
            404: "Кошелек не найден",
            400: "Неверный формат UUID"
        },
        tags=['wallets']
    )
    def retrieve(self, request: Request, wallet_id: str = None) -> Optional[Response]:
        """
        Получение баланса конкретного кошелька.

        Возвращает текущий баланс кошелька в минимальных денежных единицах (копейках/центах).
        """

        try:
            wallet = self.get_object()
            return Response({'balance': float(wallet.balance)}, status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response(
                {'error': f'Кошелек с UUID {wallet_id} не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {'error': f'Неверный формат UUID: {wallet_id}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        operation_description="Получение подробной информации о кошельке",
        responses={
            200: WalletSerializer,
            404: "Кошелек не найден",
            400: "Неверный формат UUID"
        },
        tags=['wallets']
    )
    @action(detail=True, methods=['get'])
    def info(self, request: Request, wallet_id: str = None) -> Optional[Response]:
        """
        Получение детальной информации о кошельке.

        Возвращает полную информацию о кошельке, включая:
        * UUID кошелька
        * Информацию о владельце
        * Текущий баланс
        * Дату создания
        * Дату последней операции
        """

        try:
            wallet = self.get_object()
            serializer = self.get_serializer(wallet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response(
                {'error': f'Кошелек с UUID {wallet_id} не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {'error': f'Неверный формат UUID: {wallet_id}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        operation_description="""
            Выполнение финансовой операции с кошельком.
            Поддерживаются следующие типы операций:
            * DEPOSIT - пополнение баланса
            * WITHDRAW - снятие средств
            Все операции выполняются атомарно с использованием транзакций базы данных.
            При попытке снятия проверяется достаточность средств на балансе.
            """,
        request_body=WalletOperationSerializer,
        responses={
            200: openapi.Response(
                description="Операция выполнена успешно",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Сообщение об успешном выполнении"
                        ),
                        'new_balance': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description="Новый баланс кошелька после операции"
                        )
                    }
                )
            ),
            400: "Некорректные данные операции или недостаточно средств",
            404: "Кошелек не найден",
        },
        tags=['wallets']
    )
    @action(detail=True, methods=['post'])
    def operation(self, request: Request, wallet_id: str = None) -> Response:
        """
        Выполнение финансовых операций с кошельком.
        """

        try:
            wallet = self.get_object()
            serializer = WalletOperationSerializer(data=request.data)

            if serializer.is_valid():
                perform_operation(
                    wallet_id,
                    serializer.validated_data['operation_type'],
                    serializer.validated_data['amount']
                )

                wallet.refresh_from_db()

                return Response(
                    {
                        'message': 'Операция выполнена успешно.',
                        'new_balance': float(wallet.balance)
                    },
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:  # Ловим Http404, который выбрасывается self.get_object()
            return Response(
                {'error': f'Кошелек с UUID {wallet_id} не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Необработанное исключение: {str(e)}", exc_info=True)

            return Response(
                {'error': 'Произошла ошибка обработки запроса. Пожалуйста, проверьте данные и повторите попытку.'},
                status=status.HTTP_400_BAD_REQUEST
            )
