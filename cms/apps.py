from django.apps import AppConfig


class CmsConfig(AppConfig):
    name = 'cms'

email_check_template = '''
    <html>

        <body>
            <p> 欢迎注册本服务 </p>
            <p> 这是你的用户名 : {username}</p>
            <p> 确认无误点击此链接验证</p>
            <a href="{token}">点我</a>
        </body>
    </html>
'''