from GUI_WebScrap_AI import Task, PersonalAssistantGUI

def main():
    test_add_task()
    test_edit_task()
    test_delete_task()
    
def test_add_task():
    assistant_gui = PersonalAssistantGUI()
    task = Task("Task 1", "2023-06-30")
    assistant_gui.task_manager.add_task(task)  
    tasks = assistant_gui.task_manager.get_all_tasks()
    assert len(tasks) == 1

def test_edit_task():
    assistant_gui = PersonalAssistantGUI()
    task_manager = assistant_gui.task_manager

    # Add a task
    task = Task("Task 1", "2023-06-30")
    task_manager.add_task(task)

    # Perform the edit operation
    assistant_gui.edit_task()

    # Retrieve the updated task
    tasks = task_manager.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].description == "Task 1"
    assert tasks[0].due_date == "2023-06-30"

def test_delete_task():
    assistant_gui = PersonalAssistantGUI()
    task = Task("Task 1", "2023-06-30")
    assistant_gui.task_manager.add_task(task)
    assistant_gui.delete_task()
    tasks = assistant_gui.task_manager.get_all_tasks()
    assert len(tasks) == 0

if __name__ == "__main__":
    main()