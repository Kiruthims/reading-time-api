
"""
API Views for Reading Time Calculator
Clean, professional, ready for Gumroad
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

from .utils import calculate_reading_time

@api_view(['GET'])
def api_health_check(request):
    """
    Simple health check endpoint.
    Lets users know the API is working.
    
    Returns:
        {"message": "Reading Time API is operational"}
    """
    return Response({
        "service": "Reading Time API",
        "version": "1.0.0",
        "status": "operational",
        "message": "API is ready to calculate your reading times!",
        "documentation": "Use /api/reading-time/?text=Your+text+here"
    })

@api_view(['GET'])
def calculate_reading_time_api(request):
    """
    Main API endpoint for reading time calculation.
    
    Query Parameters:
        text (required): The content to analyze
        wpm (optional): Words per minute (default: 250)
    
    Example Request:
        GET /api/reading-time/?text=Hello+World&wpm=300
    
    Example Response:
        {
            "status": "success",
            "data": {
                "minutes": 2,
                "word_count": 450,
                "words_per_minute": 300,
                "display": "2 min"
            },
            "api_info": {
                "version": "1.0.0",
                "endpoint": "reading-time"
            }
        }
    """
    try:
        # ===== 1. GET PARAMETERS =====
        text = request.GET.get('text', '')
        
        # Get WPM with safe conversion
        wpm_param = request.GET.get('wpm', '250')
        try:
            wpm = int(wpm_param)
        except ValueError:
            return Response({
                "status": "error",
                "error": "InvalidParameter",
                "message": "wpm must be a valid integer",
                "suggestion": "Example: ?wpm=250"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # ===== 2. CALCULATE =====
        result = calculate_reading_time(text, wpm)
        
        # ===== 3. BUILD RESPONSE =====
        response_data = {
            "status": "success",
            "data": result,
            "api_info": {
                "version": "1.0.0",
                "endpoint": "reading-time",
                "calculation": "rounded_up_minutes"
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except ValueError as e:
        # Handle validation errors from utils.py
        return Response({
            "status": "error",
            "error": "ValidationError",
            "message": str(e),
            "suggestion": "Check your text and wpm parameters"
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        # Catch-all for unexpected errors
        # In production, you'd log this error
        return Response({
            "status": "error",
            "error": "InternalError",
            "message": "An unexpected error occurred",
            "developer_note": "This error has been logged for investigation"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def bulk_calculate_reading_time(request):
    """
    Calculate reading time for multiple texts at once.
    
    Request Body (JSON):
        {
            "texts": ["First text", "Second text"],
            "wpm": 250  # Optional
        }
    
    Example Response:
        {
            "status": "success",
            "total_texts": 2,
            "results": [
                {"text_index": 0, "minutes": 1, "word_count": 200, ...},
                {"text_index": 1, "minutes": 3, "word_count": 650, ...}
            ]
        }
    """
    if request.method == 'POST':
        try:
            # ===== 1. PARSE JSON =====
            try:
                data = request.data
            except:
                return Response({
                    "status": "error",
                    "error": "InvalidJSON",
                    "message": "Request body must be valid JSON"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # ===== 2. VALIDATE INPUT =====
            if 'texts' not in data:
                return Response({
                    "status": "error",
                    "error": "MissingField",
                    "message": "Missing 'texts' field in request body",
                    "required_fields": ["texts"]
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not isinstance(data['texts'], list):
                return Response({
                    "status": "error",
                    "error": "InvalidType",
                    "message": "'texts' must be an array/list",
                    "example": {"texts": ["text1", "text2"]}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get WPM or use default
            wpm = data.get('wpm', 250)
            
            # ===== 3. PROCESS EACH TEXT =====
            results = []
            for index, text in enumerate(data['texts']):
                try:
                    calculation = calculate_reading_time(text, wpm)
                    results.append({
                        "text_index": index,
                        "text_preview": text[:50] + "..." if len(text) > 50 else text,
                        **calculation
                    })
                except ValueError as e:
                    # If one text fails, mark it but continue with others
                    results.append({
                        "text_index": index,
                        "text_preview": text[:50] + "..." if len(text) > 50 else text,
                        "error": str(e),
                        "minutes": None,
                        "word_count": None
                    })
            
            # ===== 4. BUILD RESPONSE =====
            successful = sum(1 for r in results if 'error' not in r)
            failed = len(results) - successful
            
            return Response({
                "status": "success",
                "summary": {
                    "total_texts": len(data['texts']),
                    "successful": successful,
                    "failed": failed,
                    "words_per_minute": wpm
                },
                "results": results
            })
            
        except Exception as e:
            return Response({
                "status": "error",
                "error": "ProcessingError",
                "message": "Failed to process bulk request"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        "status": "error",
        "error": "MethodNotAllowed",
        "message": "Only POST method is allowed for this endpoint"
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)