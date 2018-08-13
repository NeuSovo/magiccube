from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'utils'


email_check_template = '''
<table align="center"  cellpadding="0"  cellspacing="0"  style="border-collapse: collapse; border:1px solid #e5e5e5;box-shadow: 0 10px 15px rgba(0, 0, 0, 0.05);text-align: left; width:800px;">
    <tbody>
        <tr>
            <td style="padding:20px 0 10px 0;text-indent:25px;">
                <img src="javascript:;"  style="vertical-align: middle;" />
            </td>
            <tr>
                <td style="padding:10px 0;text-indent:25px;"><b>欢迎加入SSZ国际魔方联赛!</b></td>
            </tr>
            <tr>
                <td style="padding:10px 0;text-indent:25px;line-height: 10px;">
                    <p>亲爱的用户，{username},你好!</p>
                </td>
            </tr>
            <tr>
                <td style="padding:10px 0;text-indent:25px;">请点击以下链接验证你的邮箱地址! </td>
            </tr>
            <tr>
                <td style="padding:10px 0;text-indent:25px;"><a style="color:#1e88e5;text-decoration: none;"  href="{token}"  target="viewport">{token}</a></td>
            </tr>
            <tr>
                <td style="padding:10px 0;text-indent:25px;">如果以上链接无法访问，请将该网址复制并粘贴至新的浏览器窗口中。</td>
            </tr>
            <tr>
                <td style="padding:10px 0 20px 0;text-indent:25px;line-height: 10px;">
                    <p>祝您生活愉快，工作顺利！</p>
                </td>
            </tr>
        </tr>
    </tbody>
</table>
'''


email_forget_template = '''
 <table align="center"  cellpadding="0"  cellspacing="0"  style="border-collapse: collapse; border:1px solid #e5e5e5;box-shadow: 0 10px 15px rgba(0, 0, 0, 0.05);text-align: left; width:800px;">
    <tbody>
        <tr>
            <td style="padding:20px 0 10px 0;text-indent:25px;">
                <img src="javascript:;"  style="vertical-align: middle;" />
            </td>
            <tr>
                <td style="padding:10px 0;text-indent:25px;"><b>欢迎使用SSZ国际魔方联赛!</b></td>
            </tr>
            <tr>
                <td style="padding:10px 0;text-indent:25px;line-height: 10px;">
                    <p>亲爱的用户,你好!，请确认你的邮件连接{email}</p>
                </td>
            </tr>
            <tr>
                <td style="padding:10px 0;text-indent:25px;">请点击以下链接修改你的密码 ! </td>
            </tr>
            <tr>
                <td style="padding:10px 0;text-indent:25px;">注意此链接只有10分钟有效时间 ! </td>
            </tr>
            <tr>
                <td style="padding:10px 0;text-indent:25px;"><a style="color:#1e88e5;text-decoration: none;"  href="{token}"  target="viewport">{token}</a></td>
            </tr>
            <tr>
                <td style="padding:10px 0;text-indent:25px;">如果以上链接无法访问，请将该网址复制并粘贴至新的浏览器窗口中。</td>
            </tr>
            <tr>
                <td style="padding:10px 0 20px 0;text-indent:25px;line-height: 10px;">
                    <p>祝您生活愉快，工作顺利！</p>
                </td>
            </tr>
        </tr>
    </tbody>
</table>
'''

email_bind_template = '''
 <table align="center"  cellpadding="0"  cellspacing="0"  style="border-collapse: collapse; border:1px solid #e5e5e5;box-shadow: 0 10px 15px rgba(0, 0, 0, 0.05);text-align: left; width:800px;">
    <tbody>
        <tr>
            <td style="padding:20px 0 10px 0;text-indent:25px;">
                <img src="javascript:;"  style="vertical-align: middle;" />
            </td>
            <tr>
                <td style="padding:10px 0;text-indent:25px;"><b>欢迎使用SSZ国际魔方联赛!</b></td>
            </tr>
            <tr>
                <td style="padding:10px 0;text-indent:25px;line-height: 10px;">
                    <p>亲爱的用户,你好!，请确认你要绑定的邮箱地址：{email}</p>
                </td>
            </tr>
            <tr>
                <td style="padding:10px 0;text-indent:25px;">请点击以下链接确认 ! </td>
            </tr>
            <tr>
                <td style="padding:10px 0;text-indent:25px;">注意此链接只有10分钟有效时间 ! </td>
            </tr>
            <tr>
                <td style="padding:10px 0;text-indent:25px;">如果你是第一次绑定邮箱，请重置密码即可使用此邮箱登陆 !! </td>
            </tr>
            <tr>
                <td style="padding:10px 0;text-indent:25px;"><a style="color:#1e88e5;text-decoration: none;"  href="{token}"  target="viewport">{token}</a></td>
            </tr>
            <tr>
                <td style="padding:10px 0;text-indent:25px;">如果以上链接无法访问，请将该网址复制并粘贴至新的浏览器窗口中。</td>
            </tr>
            <tr>
                <td style="padding:10px 0 20px 0;text-indent:25px;line-height: 10px;">
                    <p>祝您生活愉快，工作顺利！</p>
                </td>
            </tr>
        </tr>
    </tbody>
</table>
'''
