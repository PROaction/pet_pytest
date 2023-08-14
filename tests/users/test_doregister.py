import allure


@allure.story('Users')
@allure.feature('/doregister')
@allure.title('Create user')
def test_T1(users_api, request, delete_user_after_test):
    request.node.email = 'sergey@mail.ru'
    json = {
        "email": "sergey@mail.ru",
        "name": "Sergey",
        "password": 123
    }

    users_api.doregister(json=json)
    assert users_api.name == 'Sergey'
    assert 'default_avatar.jpg' in users_api.avatar
    assert users_api.password
    assert users_api.birthday == 0
    assert users_api.email == 'sergey@mail.ru'
    assert not users_api.gender
    assert users_api.date_start == 0
    assert not users_api.hobby

    assert users_api.count_body_fields == 8
    assert users_api.http_status == 200
