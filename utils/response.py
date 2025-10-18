from rest_framework.response import Response
from rest_framework import status

class ResponseMixin:
    @staticmethod
    def success_response( data=None, message="Success", status_code=status.HTTP_200_OK):
        return Response({
            "status": "success",
            "message": message,
            "data": data,
        }, status=status_code)


    @staticmethod
    def success_response_paginated(
        paginator=None,
        data=None,
        message="Success",
        status_code= status.HTTP_200_OK
    ):
        if paginator is None:
            return
        count= paginator.page.paginator.count,
        total_pages= paginator.page.paginator.num_pages,
        current_page=paginator.page.number,
        next_page=paginator.get_next_link(),
        previous_page=paginator.get_previous_link(),
        response = {
            "count":count[0],
            "total_pages":total_pages[0],
            "current_page":current_page[0],
            "next_page":next_page[0],
            "previous_page":previous_page[0],
            "data":data,
        }
        return Response({
            "status":"success",
            "data": response,
            "message": message,
        }, status=status_code)


    @staticmethod
    def error_response( error=None, message="Error occurred", status_code=status.HTTP_400_BAD_REQUEST):
        return Response({
            "status": "error",
            "message": message,
            "error": error,
        }, status=status_code)

    @staticmethod
    def not_found_response(message="Resource not found"):
        return ResponseMixin.error_response(
            message=message,
            error="not_found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    @staticmethod
    def unauthorized_response(message="Unauthorized"):
        return ResponseMixin.error_response(
            message=message,
            error="unauthorized",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    @staticmethod
    def validation_error_response( errors, message="Validation failed"):
        return ResponseMixin.error_response(
            message=message,
            error=errors,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    @staticmethod
    def server_error_response( message="Internal server error"):
        return ResponseMixin.error_response(
            message=message,
            error="internal_server_error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )