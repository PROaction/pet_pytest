import allure


@allure.story('Users')
@allure.feature('/useronefield')
@allure.title('Updating one field from the user')
def test_T2(users_api, request, delete_user_after_test):
    request.node.email = 'sergey@mail.ru'
    json = {
        "email": "sergey@mail.ru",
        "name": "Sergey",
        "password": 123
    }
    # 1. Create User
    users_api.doregister(json=json)
    assert users_api.email

    json = {
        "email": "sergey@mail.ru",
        "field": "gender",
        "value": "m"
    }
    # 2. Update User
    users_api.useronefield(json=json)
    assert users_api.message == ('Поле gender успешно изменено на '
                                 'm у пользователя с email sergey@mail.ru')

    json = {
        "email": "sergey@mail.ru"
    }
    # 3. Get User
    users_api.getuser(json=json)
    assert users_api.gender == 'm'
