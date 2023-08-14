import allure


@allure.story('Users')
@allure.feature('/createtask')
@allure.title('Check the assigned of the task to the user')
def test_T3(users_api, tasks_api, request,
            delete_task_after_test, delete_user_after_test):
    request.node.email = 'sergey@mail.ru'
    request.node.email_owner = 'sergey@mail.ru'

    json = {
        "email": "sergey@mail.ru",
        "name": "Sergey",
        "password": 123
    }
    # 1. Create User
    users_api.doregister(json=json)
    assert users_api.email

    json = {
        "task_title": "test_task",
        "task_description": "task_description",
        "email_owner": "sergey@mail.ru",
        "email_assign": "sergey@mail.ru"
    }
    # 2. Create Task
    tasks_api.createtask(json=json)
    assert tasks_api.type == 'success'
    assert isinstance(tasks_api.id_task, int)
    assert tasks_api.message == 'Задача успешно создана!'
    request.node.id_task = tasks_api.id_task

    json = {
        "email": "sergey@mail.ru"
    }
    # 3. Check to assigned Task
    users_api.getuserfull(json=json)
    assert users_api.tasks[0] == {
        "name": "test_task",
        "id_task": tasks_api.id_task
    }
