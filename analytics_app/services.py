def calculate_average(marks):
    if not marks:
        return 0
    total = sum(mark.marks_obtained for mark in marks)
    return total / len(marks)


def get_suggestions(average, attendance):
    if attendance < 75:
        return "Improve attendance."
    if average < 40:
        return "Focus more on weak subjects."
    return "Good performance. Keep it up!"