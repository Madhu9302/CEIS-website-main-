from pydantic import BaseModel, EmailStr, Field, ConfigDict

class ContactRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=30)
    message: str = Field(..., min_length=5, max_length=5000)
    website_url: str | None = Field(default=None, description="Honeypot field - leave empty")

class QuoteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=30)
    company: str | None = Field(default=None, max_length=150)
    service_interest: str = Field(..., min_length=2, max_length=150)
    budget_range: str | None = Field(default=None, max_length=100)
    message: str = Field(..., min_length=5, max_length=5000)
    website_url: str | None = Field(default=None, description="Honeypot field - leave empty")

class PublicSubmissionResponse(BaseModel):
    message: str