import pytest
from unittest.mock import Mock, patch
from src.auth import get_current_user_id
from fastapi import HTTPException
from jwt import PyJWKClient, ExpiredSignatureError, InvalidTokenError


class TestJWTVerification:
    @pytest.fixture
    def mock_request(self):
        request = Mock()
        request.state = Mock()
        return request

    @pytest.fixture
    def valid_token(self):
        return "valid.jwt.token"

    @pytest.fixture
    def expired_token(self):
        return "expired.jwt.token"

    @pytest.fixture
    def invalid_token(self):
        return "invalid.token"

    @patch("src.auth.jwks_client")
    @patch("src.auth.jwt.decode")
    async def test_valid_token_returns_user_id(
        self, mock_decode, mock_jwks, mock_request, valid_token
    ):
        mock_jwks.get_signing_key_from_jwt.return_value = Mock(key="test-key")
        mock_decode.return_value = {"sub": "user-123"}

        result = await get_current_user_id(
            mock_request,
            Mock(credentials=valid_token),
        )

        assert result == "user-123"
        assert mock_request.state.user_id == "user-123"

    @patch("src.auth.jwks_client")
    @patch("src.auth.jwt.decode")
    async def test_expired_token_raises_401(
        self, mock_decode, mock_jwks, mock_request, expired_token
    ):
        mock_jwks.get_signing_key_from_jwt.return_value = Mock(key="test-key")
        mock_decode.side_effect = ExpiredSignatureError()

        with pytest.raises(HTTPException) as exc_info:
            await get_current_user_id(
                mock_request,
                Mock(credentials=expired_token),
            )

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Token expired"

    @patch("src.auth.jwks_client")
    @patch("src.auth.jwt.decode")
    async def test_invalid_token_raises_401(
        self, mock_decode, mock_jwks, mock_request, invalid_token
    ):
        mock_jwks.get_signing_key_from_jwt.return_value = Mock(key="test-key")
        mock_decode.side_effect = InvalidTokenError()

        with pytest.raises(HTTPException) as exc_info:
            await get_current_user_id(
                mock_request,
                Mock(credentials=invalid_token),
            )

        assert exc_info.value.status_code == 401

    async def test_missing_token_raises_401(self, mock_request):
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user_id(mock_request, None)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Not authenticated"