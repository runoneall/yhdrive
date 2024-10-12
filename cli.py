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
    import json
    from AskYunhu import FileCtrl
    import Tool

    # Load File List
    MetaJsonList = [file for file in os.listdir(MetaJsonFolder) if not file.startswith('.')]
    if MetaJsonList == []:
        print('没有可供下载的文件')
        exit()
    print('\n     可下载列表')
    print('--------------------')
    for Item in MetaJsonList:
        print(f' {MetaJsonList.index(Item)+1}) {os.path.splitext(os.path.basename(Item))[0]}')
    
    # Pick File
    FileId = int(input('\n下载: '))-1
    FileName = MetaJsonList[FileId]
    print(f'读取元信息 {FileName}')

    # Read MetaJson
    with open(f'{MetaJsonFolder}/{FileName}', 'r', encoding='utf-8') as metajson_file:
        metajson = json.load(metajson_file)
    target_name = metajson["name"]
    target_chunks = metajson["chunks"]
    print('\n     文件信息')
    print('------------------')
    print(f' 名称: {target_name}')
    print(f' 块数量: {len(target_chunks)}')

    # Download File
    Tool.CleanDir()
    if input('\n确定要下载吗? (Y/n) > ') == 'n':
        print('取消下载')
        exit()
    with open(f"./cache/{target_name}", "wb") as file:
        pass
    for ChunkId in target_chunks:
        print(f'下载块 {ChunkId}')
        Content = FileCtrl.Download(ChunkId)
        with open(f"./cache/{target_name}", "ab") as file:
            file.write(Content)
    print(f'文件已保存 ./cache/{target_name}')