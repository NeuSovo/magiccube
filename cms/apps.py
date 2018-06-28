from django.apps import AppConfig


class CmsConfig(AppConfig):
    name = 'cms'

email_check_template = '''
      <table align="center"  cellpadding="0"  cellspacing="0"  style="border-collapse: collapse; border:1px solid #e5e5e5;box-shadow: 0 10px 15px rgba(0, 0, 0, 0.05);text-align: left; width:800px;">
        <tbody>
        <tr>
                <td style="padding:20px 0 10px 0;text-indent:25px;">
                    <img src="javascript:;"  style="vertical-align: middle;" />
                </td>
            </tr>
            <tr>
                <td style="padding:10px 0;text-indent:25px;"><b>欢迎加入顺时针魔方!</b></td>
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
        </tbody>
    </table>
'''