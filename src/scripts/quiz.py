"""Telegram quiz bot — generates questions from module fiches using Claude."""

import os
from datetime import date
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from loguru import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

load_dotenv()

MODULES_DIR = Path(__file__).parent.parent.parent / "modules"
ERRORS_LOG = Path(__file__).parent.parent.parent / "errors-and-lessons" / "log.md"
QUESTIONS_PER_SESSION = 5

SELECTING_MODULE = 0
ANSWERING = 1


def discover_non_empty_modules(modules_dir: Path) -> list[tuple[str, Path]]:
    """Return (slug, fiche_path) for fiches with content beyond the header line."""
    result = []
    for fiche in sorted(modules_dir.glob("**/*_fiche.md")):
        lines = [line for line in fiche.read_text().splitlines() if line.strip()]
        if len(lines) > 1:
            slug = fiche.stem.replace("_fiche", "")
            result.append((slug, fiche))
    return result


def generate_questions(fiche_content: str, n: int = QUESTIONS_PER_SESSION) -> list[str]:
    """Call Claude to generate n questions from fiche content."""
    client = anthropic.Anthropic()
    prompt = (
        f"Based on the following study notes, generate exactly {n} concise quiz questions. "
        "Return ONLY the questions, one per line, numbered 1. 2. 3. etc. No answers.\n\n"
        f"{fiche_content}"
    )
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text
    questions = [line.split(". ", 1)[1].strip() for line in raw.strip().splitlines() if ". " in line]
    return questions[:n]


def evaluate_answer(question: str, answer: str, fiche_content: str) -> tuple[bool, str]:
    """Return (is_correct, feedback) by asking Claude to evaluate the answer."""
    client = anthropic.Anthropic()
    prompt = (
        f"Study notes:\n{fiche_content}\n\n"
        f"Question: {question}\n"
        f"Student answer: {answer}\n\n"
        "Evaluate the answer. First line must be exactly CORRECT or INCORRECT. "
        "Then a 1-2 sentence explanation."
    )
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    lines = message.content[0].text.strip().splitlines()
    is_correct = lines[0].strip().upper().startswith("CORRECT")
    explanation = " ".join(lines[1:]).strip()
    return is_correct, explanation


def log_error(slug: str, question: str, answer: str, feedback: str) -> None:
    """Append a wrong answer entry to the errors log."""
    entry = f"\n## [{date.today()}] Quiz error — {slug}\n**Q**: {question}\n**A**: {answer}\n**Feedback**: {feedback}\n"
    ERRORS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with ERRORS_LOG.open("a") as f:
        f.write(entry)


# ── Telegram handlers ────────────────────────────────────────────────────────


async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    modules = discover_non_empty_modules(MODULES_DIR)
    if not modules:
        await update.message.reply_text("No modules available yet.")
        return ConversationHandler.END

    context.user_data["modules"] = modules
    keyboard = [[InlineKeyboardButton(slug, callback_data=str(i))] for i, (slug, _) in enumerate(modules)]
    await update.message.reply_text("Choose a module:", reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECTING_MODULE


async def module_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    idx = int(query.data)
    slug, fiche_path = context.user_data["modules"][idx]
    fiche_content = fiche_path.read_text()
    questions = generate_questions(fiche_content)

    context.user_data.update(
        {
            "slug": slug,
            "fiche_content": fiche_content,
            "questions": questions,
            "current": 0,
            "score": 0,
        }
    )

    await query.edit_message_text(f"*{slug}* — {len(questions)} questions", parse_mode="Markdown")
    await query.message.reply_text(f"Q1: {questions[0]}")
    return ANSWERING


async def receive_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    data = context.user_data
    idx = data["current"]
    question = data["questions"][idx]
    answer = update.message.text

    is_correct, feedback = evaluate_answer(question, answer, data["fiche_content"])

    if is_correct:
        data["score"] += 1
        await update.message.reply_text(f"Correct! {feedback}".strip())
    else:
        log_error(data["slug"], question, answer, feedback)
        await update.message.reply_text(f"Wrong. {feedback}".strip())

    data["current"] += 1
    if data["current"] < len(data["questions"]):
        next_q = data["questions"][data["current"]]
        await update.message.reply_text(f"Q{data['current'] + 1}: {next_q}")
        return ANSWERING

    score = data["score"]
    total = len(data["questions"])
    await update.message.reply_text(f"Done! Score: {score}/{total}")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Quiz cancelled.")
    return ConversationHandler.END


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Unhandled exception", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(f"Error: {context.error}")


def main() -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    app = Application.builder().token(token).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("quiz", start_quiz)],
        states={
            SELECTING_MODULE: [CallbackQueryHandler(module_selected)],
            ANSWERING: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_answer)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
    app.add_error_handler(error_handler)
    logger.info("Bot started.")
    app.run_polling()


if __name__ == "__main__":
    main()
