import vk_api

from Configurations.vk_module_config import login, password


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


if __name__ == '__main__':
    vk_session = vk_api.VkApi(login=login, password=password, auth_handler=auth_handler)
    try:
        vk_session.auth()
    except vk_api.AuthError as e:
        print(e)
    vk = vk_session.get_api()
    response = vk.wall.get(domain='nycoffee_samara', count=1)
    if response['items']:
        print(response['items'][0]['text'])
