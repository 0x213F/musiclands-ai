import uuid
import time
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from services.chatgpt_service import chatgpt_service
from models.llm.requests import (
    ComplexLLMRequest, 
    LLMQueryResponse, 
    TimeRangeExtractionResponse, 
    QueryType,
    BatchLLMRequest,
    BatchLLMResponse,
    TimeRange
)
from prompts.time_range_extractor import TimeRangeExtractorPrompt

class LLMPromptService:
    """Service for managing complex LLM queries with different prompt types"""
    
    def __init__(self):
        self.chatgpt = chatgpt_service
        self.time_range_extractor = TimeRangeExtractorPrompt()
        
    async def process_query(self, request: ComplexLLMRequest) -> LLMQueryResponse:
        """
        Process a complex LLM query based on its type
        
        Args:
            request: Complex LLM request with context
            
        Returns:
            Structured LLM response
        """
        start_time = time.time()
        request_id = str(uuid.uuid4())
        
        try:
            if request.query_type == QueryType.TIME_RANGE_EXTRACTION:
                response_data = await self._process_time_range_extraction(request)
            elif request.query_type == QueryType.ACTIVITY_RECOMMENDATION:
                response_data = await self._process_activity_recommendation(request)
            elif request.query_type == QueryType.MUSIC_DISCOVERY:
                response_data = await self._process_music_discovery(request)
            else:
                # Default conversation handling
                response_data = await self._process_conversation(request)
            
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            return LLMQueryResponse(
                request_id=request_id,
                query_type=request.query_type,
                response_data=response_data,
                processing_time_ms=processing_time_ms,
                error=None
            )
            
        except Exception as e:
            processing_time_ms = int((time.time() - start_time) * 1000)
            return LLMQueryResponse(
                request_id=request_id,
                query_type=request.query_type,
                response_data={},
                processing_time_ms=processing_time_ms,
                error=str(e)
            )

    async def _process_time_range_extraction(self, request: ComplexLLMRequest) -> Dict[str, Any]:
        """Process time range extraction queries"""
        if not self.chatgpt.is_available():
            raise Exception("ChatGPT service is not available")
        
        # Build location context if available
        user_location = None
        if request.location:
            user_location = {
                'lat': request.location.lat,
                'lng': request.location.lng
            }
        
        # Build prompt
        prompt = self.time_range_extractor.build_prompt(
            user_query=request.query,
            current_time=request.time_context.current_time,
            user_location=user_location,
            timezone_info=request.time_context.timezone
        )
        
        # Get LLM response
        raw_response = self.chatgpt.chat_completion(
            message=prompt,
            model="gpt-3.5-turbo",
            max_tokens=800,
            temperature=0.3  # Lower temperature for more consistent structured output
        )
        
        if not raw_response:
            raise Exception("Failed to get LLM response")
        
        # Parse structured response
        parsed_data = self.time_range_extractor.parse_response(raw_response)
        if not parsed_data:
            raise Exception("Failed to parse structured response from LLM")
        
        # Convert to our response model
        time_range_data = parsed_data['time_range']
        time_range = TimeRange(
            start_time=datetime.fromisoformat(time_range_data['start_time']),
            end_time=datetime.fromisoformat(time_range_data['end_time']),
            description=time_range_data['description']
        )
        
        response = TimeRangeExtractionResponse(
            time_range=time_range,
            reasoning=parsed_data['reasoning'],
            confidence=parsed_data['confidence'],
            query_type=parsed_data['query_type'],
            raw_llm_response=raw_response
        )
        
        return response.dict()

    async def _process_activity_recommendation(self, request: ComplexLLMRequest) -> Dict[str, Any]:
        """Process activity recommendation queries"""
        # This is a placeholder - you can expand this with activity-specific prompts
        
        context_parts = []
        
        # Add time context
        time_info = f"Current time: {request.time_context.current_time.strftime('%A, %B %d, %Y at %I:%M %p')}"
        if request.time_context.timezone:
            time_info += f" ({request.time_context.timezone})"
        context_parts.append(time_info)
        
        # Add location context
        if request.location:
            location_info = f"Location: {request.location.lat}, {request.location.lng}"
            if request.location.city:
                location_info += f" ({request.location.city})"
            context_parts.append(location_info)
        
        # Add user context
        if request.user_context and request.user_context.display_name:
            context_parts.append(f"User: {request.user_context.display_name}")
        
        context = "\n".join(context_parts)
        
        system_prompt = f"""You are an activity recommendation assistant. Based on the user's query and context, provide personalized activity suggestions.

Context:
{context}

Provide helpful, location-aware, and time-appropriate activity recommendations."""
        
        response = self.chatgpt.chat_completion(
            message=request.query,
            system_prompt=system_prompt,
            model="gpt-3.5-turbo",
            max_tokens=800,
            temperature=0.7
        )
        
        return {"recommendation": response, "context": context}

    async def _process_music_discovery(self, request: ComplexLLMRequest) -> Dict[str, Any]:
        """Process music discovery queries"""
        user_context = {}
        if request.user_context:
            if request.user_context.display_name:
                user_context["display_name"] = request.user_context.display_name
            if request.user_context.preferences:
                user_context.update(request.user_context.preferences)
        
        response = self.chatgpt.music_chat_completion(request.query, user_context)
        return {"music_response": response, "user_context": user_context}

    async def _process_conversation(self, request: ComplexLLMRequest) -> Dict[str, Any]:
        """Process general conversation queries"""
        response = self.chatgpt.chat_completion(
            message=request.query,
            model="gpt-3.5-turbo",
            max_tokens=600,
            temperature=0.8
        )
        return {"response": response}

    async def process_batch(self, batch_request: BatchLLMRequest) -> BatchLLMResponse:
        """
        Process multiple LLM queries in batch
        
        Args:
            batch_request: Batch of LLM requests
            
        Returns:
            Batch response with all individual results
        """
        start_time = time.time()
        batch_id = str(uuid.uuid4())
        
        if batch_request.parallel:
            responses = await self._process_batch_parallel(
                batch_request.requests, 
                batch_request.max_parallel
            )
        else:
            responses = await self._process_batch_sequential(batch_request.requests)
        
        total_processing_time = int((time.time() - start_time) * 1000)
        
        successful_count = sum(1 for r in responses if r.error is None)
        failed_count = len(responses) - successful_count
        
        return BatchLLMResponse(
            batch_id=batch_id,
            responses=responses,
            total_processing_time_ms=total_processing_time,
            successful_count=successful_count,
            failed_count=failed_count
        )

    async def _process_batch_sequential(self, requests: List[ComplexLLMRequest]) -> List[LLMQueryResponse]:
        """Process requests sequentially"""
        responses = []
        for request in requests:
            response = await self.process_query(request)
            responses.append(response)
        return responses

    async def _process_batch_parallel(
        self, 
        requests: List[ComplexLLMRequest], 
        max_parallel: int
    ) -> List[LLMQueryResponse]:
        """Process requests in parallel with concurrency limit"""
        semaphore = asyncio.Semaphore(max_parallel)
        
        async def process_with_semaphore(request):
            async with semaphore:
                return await self.process_query(request)
        
        tasks = [process_with_semaphore(request) for request in requests]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert exceptions to error responses
        processed_responses = []
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                error_response = LLMQueryResponse(
                    request_id=str(uuid.uuid4()),
                    query_type=requests[i].query_type,
                    response_data={},
                    error=str(response)
                )
                processed_responses.append(error_response)
            else:
                processed_responses.append(response)
        
        return processed_responses

# Global LLM prompt service instance
llm_prompt_service = LLMPromptService()