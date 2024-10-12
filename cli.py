import os

MetaJsonFolder = './MetaJson'
if not os.path.exists(MetaJsonFolder):
    os.makedirs(MetaJsonFolder)

print('''
功能:
  (1) 上传文件
  (2) 下载文件''')
mode = input('> ')

if mode == '1':
    from AskYunhu import User
    from AskYunhu import FileCtrl
    import Tool

    # Login
    LoginRep = User.Login(
        input('\n登入邮箱: '), 
        input('登入密码: '), 
        'yhdrive'
    )
    if LoginRep['msg'] != 'success':
        print('验证失败')
        exit(1)
    print('登入成功')
    UserToken = LoginRep['data']['token']

    # Cut File
    Tool.CleanDir()
    FilePath = input('文件路径: ')
    ChunkList = Tool.CutFile(
        TargetFilePath=FilePath,
        TargetChunkSize=20
    )

    # Upload File
    if input('确认上传? (Y/n) > ') == 'n':
        print('取消上传')
        print('正在清理')
        Tool.CleanDir()
        exit()
    print('正在上传')
    ChunkItems = list()
    for Item in ChunkList:
        print(f'上传 {os.path.basename(Item)}')
        with open(Item, 'rb') as file:
            binary_data = file.read()
        RepJson = FileCtrl.Upload(binary_data, UserToken)
        ChunkItems.append(RepJson['key'])
    
    # Make Meta Json
    print('正在保存元信息')
    FileName = os.path.basename(FilePath)
    FileName = FileName.replace(' ', '_')
    SavePath = f"{MetaJsonFolder}/{FileName}.json"
    Tool.MetaJsonMaker(FileName, ChunkItems, SavePath)
    print('元信息已保存')

    # Finish
    print('正在清理')
    Tool.CleanDir()
    print('上传完成')

if mode == '2':
    from AskYunhu import FileCtrl

    # Load MetaJson List
    MetaJsonList = os.listdir(MetaJsonFolder)
    print(MetaJsonList)