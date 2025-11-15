from statements.ai.tasks import analyze_statement_task

if __name__ == "__main__":
    statement_id = 2  # Burayı istediğin gibi değiştir
    result = analyze_statement_task.delay(statement_id)
    print(f"Task {result.id} gönderildi.")
