# BeautyFlow AI

BeautyFlow is a multilingual prototype for handling beauty-studio enquiries. A language model extracts what the customer is asking for; Python applies business rules and routes sensitive or unsupported requests to a person.

> The model interprets. The workflow decides. People handle exceptions.

All studio details and business data in this repository are synthetic. This is a learning project, not a live booking service.

## How it works

```text
customer message -> Gemini extraction -> validation -> Python date and safety rules
                                                       -> grounded reply or human review
```

- Understands messages in Spanish, English and German.
- Uses deterministic Python rules for date resolution and routing.
- Grounds replies in `knowledge_base.json`; it does not invent missing prices or confirm appointments.
- Escalates health-related questions, complaints and unsupported cases for human review.
- Includes offline workflow checks in `test_workflow.py`.

## Run locally

Install Python 3.10 or newer, then install the dependencies:

```text
python -m pip install google-genai python-dotenv
```

Create a local `.env` file in this folder with your own Gemini API key:

```text
GEMINI_API_KEY=your_key_here
```

Keep `.env` private. It is excluded from Git by `.gitignore`; never paste the key into this repository, the website, or a public chat.

Run the offline checks (no API call required):

```text
python test_workflow.py
```

Run a sample message (uses the Gemini API):

```text
python beautyflow.py "Hi, I want to book a classic facial this Friday evening."
```

## Portfolio page

The static project page is `index.html` at the repository root. It contains a local, illustrative demo that makes no API calls. It can be published with GitHub Pages by selecting the `main` branch and the root folder as the Pages source in the repository settings.

## Current limits

- The calendar, CRM and customer-facing booking interface are not connected.
- A `check_calendar` action is a routing result; it does not check or reserve a real appointment.
- The sample business and its service information are fictional.
