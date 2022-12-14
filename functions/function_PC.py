## save img to self.img, instead of returning img
## check basic status in home_screen
## ver2:  auto eat food
## ver3: auto leave guild, detect bag full, auto open box
## ver4: fix map function
def myimport(package, module=None): # eg: cv2, opence-python
    try:
        importlib.import_module(package)
    except ImportError:
        print(ImportError)
        if type(module)==type(None):
            subprocess.call(['pip', 'install', package])
        else:
            subprocess.call(['pip', 'install', module])
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def ImgSearch(icon, img, threshold=0.8, x_scale = 1, y_scale = 1, pos=0, show=0, value=0):
    # pos: return image position
    # show: plot the given region +margin = show
    # value: print the maximum res
    if x_scale!=1:
        icon = imutils.resize(icon, width = int(icon.shape[1] * x_scale), height = int(icon.shape[0] * y_scale))
    res = cv2.matchTemplate(img, icon, cv2.TM_CCOEFF_NORMED)
    if value:
        print(np.max(res), end=' ')
    loc = np.where(res >= threshold)
    if show: # plot
        y, x = np.unravel_index(res.argmax(), res.shape)
        plt.imshow(img[y:(y+icon.shape[0]),x:(x+icon.shape[1]),])
    if pos==1: # return the maximum position
        y, x = np.unravel_index(res.argmax(), res.shape)
        return np.max(res), x+int(icon.shape[1]/2), y+int(icon.shape[0]/2)
    else:
        return sum(sum(loc))>0

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    origin = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return origin[::-1]
def rgb_to_hex(rgb):
    return '0x%02x%02x%02x' % rgb
def getIdleTime():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0
def rgba2rgb(rgba, background=(255,255,255) ):
    row, col, ch = rgba.shape
    if ch == 3:
        return rgba
    assert ch == 4, 'RGBA image has 4 channels.'
    rgb = np.zeros( (row, col, 3), dtype='float32' )
    r, g, b, a = rgba[:,:,0], rgba[:,:,1], rgba[:,:,2], rgba[:,:,3]
    a = np.asarray( a, dtype='float32' ) / 255.0
    R, G, B = background
    rgb[:,:,2] = r * a + (1.0 - a) * R
    rgb[:,:,1] = g * a + (1.0 - a) * G
    rgb[:,:,0] = b * a + (1.0 - a) * B
    return np.asarray( rgb, dtype='uint8' )

def clock(): # modula by 240 minitues
    now = datetime.now()
    hour = int(now.strftime("%H"))
    minute = int(now.strftime("%M"))
    time_now = 60*(hour%4)+minute
    print( "????????????: "+str(time_now))
    return(time_now)

def clock2(mode='minute'): # modula by 240 minitues
    tz = pytz.timezone('Asia/Taipei')
    now = datetime.now(tz)
    if mode == 'minute':
        hour = int(now.strftime("%H"))
        minute = int(now.strftime("%M"))
        t_now = hour*60+minute
    elif mode =='day':
        t_now = int(now.strftime("%j"))
    return(t_now)

def get_child_windows(parent):
    '''
    Get all child window handles for parent
    Returns a list of sub-window handles
       '''
    if not parent:
        return
    hwndChildList = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
    return hwndChildList
if character_id == 'Moonlight_Global':
    key_left = "{A}"
    key_right = "{D}"
    key_up = "{W}"
    key_pet = "{V}"
    key_friend = "{B}"
    key_bag = "{I}"
    key_list = "{O}"
    key_info = "{P}"
    key_switch = "{TAB}"
    key_back = "{ESC}"
    key_mall = '{U}'
## Moonlight_LD version
else:
    key_left = (0.4, 0.52)
    key_right = (0.6, 0.52)
    key_up = (0.5, 0.3)
    key_pet = (0.026, 0.552)
    key_friend = (0.618, 0.481)
    key_bag = (0.912, 0.055)
    key_list = (0.97, 0.054)
    key_info = (0.04,0.09)
    key_switch = (0.97, 0.883)
    key_back = 0x1B
    key_mall = (0.804, 0.061)


class Game_obj:
    import new_func1
    def __init__(self):
        ## window setup
        self.title = character_id
        ## Moonlight_PC version
        if self.title=="Moonlight_Global":
            def windowEnumerationHandler(hwnd, top_windows):
                if  win32gui.GetWindowText(hwnd)==self.title:
                    top_windows.append(hwnd)
            hwnd_lst = []  # all open windows
            win32gui.EnumWindows(windowEnumerationHandler, hwnd_lst)
            print(hwnd_lst)
            if len(hwnd_lst)>1:
                print('??????????????????????????????????????????: ')
                while win32gui.GetWindowText (win32gui.GetForegroundWindow())!="Moonlight_Global":
                    pass
                self.hwnd = win32gui.GetForegroundWindow()
            else:
                self.hwnd = hwnd_lst[0]
            self.win = Application().connect(handle=self.hwnd).window()
        ## Moonlight_LD version
        else:
            self.hwnd0 = win32gui.FindWindow(None, self.title)
            self.hwnd1 = win32gui.FindWindowEx(self.hwnd0, None, None, None)
            self.hwnd=self.hwnd1 ##operation hwnd
            self.img = self.screenshot()# last screenshot imgage
        
        ## time setup, last use time
        self.t_boss = t_boss        # last detect fightboss time
        self.t_food = t_food        # last eat food time
        self.t_auction = t_auction  # last auction time
        self.t_ep = t_ep            # ep = ena potion
        self.t_sp = t_sp            # sp = speed potion
        self.t_guild_raid = 0       # ??????????????????????????????
        self.t_debuffskill = 0      # ????????????????????????
        self.t_drinkwater = 0       # ?????????????????????
        self.d_daily = d_daily      # last daily time  [day, hour]
        self.d_hunt = d_hunt        # last daily time  [day, hour]
        self.d_pvp = d_pvp          # last daily time  [day, hour]
        self.t_eco = 0
        
        ## status setup
        self.exe = exe # execute basic functions: -1 stop, 0 check, 1 execute
        self.mode = 'basic'
        self.checkusing = checkusing
        self.boss_status = 0
        self.boss_status_max = 7
        
        # enable functions
        self.enable_auction = enable_auction
        self.enable_food = enable_food
        self.enable_daily = enable_daily
        self.enable_hunt = enable_hunt
        self.enable_raid = enable_raid
        self.enable_pvp = enable_pvp
        self.enable_debuff = enable_debuff

        # basic
        self.character_id = character_id
        self.num_resurrect = num_resurrect
        self.gap_resurrect = gap_resurrect
        self.team_accept = team_accept
        self.team_add = team_add
        self.ultimate_water = 0
        
        self.equip_basic = equip_basic
        self.statue_basic = statue_basic
        self.friend_basic = friend_basic
        self.water_basic = water_basic
        self.check_boss = check_boss
        self.time_boss = None
        
        # auction
        self.gap_auction = gap_auction

        # food
        self.key_food = key_food
        self.gap_food = gap_food
        
        # daily
        self.hour_daily = hour_daily
        self.min_daily = min_daily
        
        # guild
        self.hour_guild = hour_guild
        self.min_guild = min_guild
        self.x_guild = x_guild
        self.y_guild = y_guild
        self.enter_hunt = clock2('day')-1
        self.enter_pvp = enter_pvp
        self.leave_guild = leave_guild
        self.leave_pvp = leave_pvp

        # raid
        self.ticket_raid = ticket_raid
        self.sp_raid = sp_raid
        self.level_raid = level_raid
        self.gap_resurrect_raid = gap_resurrect_raid
        self.equip_raid = equip_raid 
        self.statue_raid = statue_raid
        self.friend_raid = friend_raid
        self.water_raid = water_raid
        self.raid_start = [540,720,900,1080,1260,1440]
        self.early_raid = early_raid
        self.raid1 = raid1
        self.raid2 = raid2
        self.raid3 = raid3
        self.raid4 = raid4
        self.raid5 = raid5
        self.raid6 = raid6
        self.key_left = key_left
        self.key_right = key_right
        self.key_up = key_up
        
        # pvp
        self.hour_start_pvp = hour_start_pvp
        self.min_start_pvp = min_start_pvp
        self.hour_end_pvp = hour_end_pvp
        self.min_end_pvp = min_end_pvp
        self.until_reward = untilreward
        self.equip_pvp = equip_pvp 
        self.statue_pvp = statue_pvp
        self.friend_pvp = friend_pvp
        self.sp_pvp = sp_pvp
        self.ep_pvp = ep_pvp
      
        # debuff solver
        self.key_debuffskill = '{'+str(key_debuffskill)+'}'  
        self.page_debuffskill = page_debuffskill


        # key
        self.key_map = "{M}"

        new_func1.print_mode(self)

        
    def save_time(self):
        print('????????????')
        file1 = open("time.py","w")
        file1.write("t_boss = "+str(self.t_boss)+"\n")
        file1.write("t_food = "+str(self.t_food)+"\n")
        file1.write("t_auction = "+str(self.t_auction)+"\n")
        file1.write("t_ep = "+str(self.t_ep)+"\n")
        file1.write("t_sp = "+str(self.t_sp)+"\n")
        file1.write("d_daily = "+str(self.d_daily)+"\n")
        file1.write("d_pvp = "+str(self.d_pvp)+"\n")
        file1.write("d_hunt = "+str(self.d_hunt)+"\n")                
        file1.close()
        
    def print_info(self):
        os.system('cls')
        print('-----------------------????????????-----------------------')
        print('??????????????????: '+ self.character_id )
        print('????????????:' + str(self.getPosition()))
        print('??????????????????: ' + str(self.num_resurrect) + ', ?????? = ' + str(self.gap_resurrect) +'???')
        if self.team_accept:
            print('??????????????????: ???')
        else:
            print('??????????????????: ???')

        if self.team_add:
            print('?????????????????????: ???')
        else:
            print('?????????????????????: ???')
        
        if self.equip_basic+self.statue_basic+self.friend_basic> 0:
            msg = '??????????????????: '
            fp = 1
            if self.equip_basic>0:
                if not fp:
                    msg = msg+', '
                fp = 0
                msg = msg+'??????='+str(self.equip_basic)
            if self.statue_basic>0:
                if not fp:
                    msg = msg+', '
                fp = 0
                msg = msg+'??????='+str(self.statue_basic)
            if self.friend_basic>0:
                if not fp:
                    msg = msg+', '
                fp = 0
                msg = msg+'??????='+str(self.friend_basic)
            if self.water_basic:
                msg = msg + ', 30% HP??????'
            else:
                msg = msg + ', 20% HP??????'
            print(msg)

        if enable_debuff:
            print('??????????????????: ??? '+str(self.page_debuffskill)+' ???, ?????? '+str(self.key_debuffskill[1]))
        else:
            print('?????????????????????')
        print(' ')
        print('-----------------------????????????-----------------------')  
        # raid
        if not self.enable_raid:
            print('??????????????????')
        elif self.level_raid==290:
            print("?????????????????????????????????")
        else:
            if self.ticket_raid:
                print('???????????? (???????????????): '+str(self.level_raid)+ ', ???????????? = ' + str(self.gap_resurrect_raid) +'???')
            else:
                print('???????????? (??????????????????): '+str(self.level_raid)+ ', ???????????? = ' + str(self.gap_resurrect_raid) +'???')
            msg = '???????????????: '
            ct=0
            for i in range(0, 6):
                if getattr(self, 'raid'+str(i+1)):
                    ct += 1
                    if ct>1:
                        msg = msg + ', '
                    msg = msg + str((self.raid_start[i]-self.early_raid)//60) + ":" + str((self.raid_start[i]-self.early_raid)%60)
            print(msg)

            if self.equip_raid+self.statue_raid+self.friend_raid> 0:
                msg = '??????????????????: '
                fp = 1
                if self.equip_raid>0:
                    if not fp:
                        msg = msg+', '
                    fp = 0
                    msg = msg+'??????='+str(self.equip_raid)
                if self.statue_raid>0:
                    if not fp:
                        msg = msg+', '
                    fp = 0
                    msg = msg+', ??????='+str(self.statue_raid)
                if self.friend_raid>0:
                    if not fp:
                        msg = msg+', '
                    fp = 0
                    msg = msg+', ??????='+str(self.friend_raid)
                print(msg)
            if self.water_raid and self.sp_raid:
                print('??????: 30%HP?????? + 30%????????????')
            elif self.water_raid:
                print('??????: 30%HP??????')
            elif self.sp_raid:
                print('??????: 30%????????????')
            else:
                print('???????????????')
        print(' ')
        print('---------------------??????????????????---------------------') 
        # hunt
        if not self.enable_hunt:
            print("????????????????????????")
        else:
            if self.min_guild<10:
                msg = "??????????????????: " + str(self.hour_guild) + ":0" + str(self.min_guild)
            else:
                msg = "??????????????????: " + str(self.hour_guild) + ":" + str(self.min_guild)
            if self.enter_hunt==clock2('day'):
                if clock2() > self.hour_guild*60 + self.min_guild + 120:
                    msg = msg + " (?????????)"
                elif clock2() > self.hour_guild*60 + self.min_guild:
                    msg = msg + " (????????????)"
            print(msg)
        print(' ')
        print('----------------------???????????????----------------------')
        tz = pytz.timezone('Asia/Taipei')
        # pvp
        if not self.enable_pvp:
            print('?????????????????????')
        elif datetime.now(tz).isoweekday()==7:
            print('???????????????????????????')
        else:
            hour_lower, min_lower = self.hour_start_pvp, self.min_start_pvp
            hour_upper, min_upper = self.hour_end_pvp, self.min_end_pvp
            msg = ''
            
            if min_lower<10:
                msg = msg + '???????????????: ' + str(hour_lower) + ":0" +str(min_lower)
            else:
                msg = msg + '???????????????: ' + str(hour_lower) + ":" +str(min_lower)

            if min_upper<10:
                msg = msg + ' ??? ' + str(hour_upper) + ":0" +str(min_upper)
            else:
                msg = msg + ' ??? ' + str(hour_upper) + ":" +str(min_upper)

            if clock2() < hour_lower*60+min_lower or clock2() > hour_upper*60+min_upper:
                msg = msg + ' (??????????????????)'
            elif self.d_pvp==clock2('day'):
                msg = msg + ' (???????????????)'
            print(msg)

            if self.until_reward:
                print('?????????????????????: ???')
            else:
                print('?????????????????????: ???')

            if self.sp_pvp and self.ep_pvp:
                print('??????: 30%???????????? + ???????????????')
            elif self.sp_pvp:
                print('??????: 30%??????')
            elif self.ep_pvp:
                print('??????: ???????????????')
            else:
                print('???????????????')
            
            if self.equip_pvp+self.statue_pvp+self.friend_pvp> 0:
                msg = '?????????????????????: '
                fp = 1 # first print
                if self.equip_pvp>0:
                    if not fp:
                        msg = msg+', '
                    fp = 0
                    msg = msg+'??????='+str(self.equip_pvp)
                if self.statue_pvp>0:
                    if not fp:
                        msg = msg+', '
                    fp = 0
                    msg = msg+'??????='+str(self.statue_pvp)
                if self.friend_pvp>0:
                    if not fp:
                        msg = msg+', '
                    fp = 0
                    msg = msg+'??????='+str(self.friend_pvp)
                print(msg)
        print(' ')
        print('-----------------------????????????-----------------------')
        # daily
        if not self.enable_daily:
            print("????????????????????????")
        else:
            d_now, h_now = clock2('day'), clock2()
            if h_now < 5:
                d_now -= 1
            if self.min_daily<10:
                msg = "??????????????????: " + str(self.hour_daily) + ":0" + str(self.min_daily)
            else:
                msg = "??????????????????: " + str(self.hour_daily) + ":" + str(self.min_daily)
            if d_now==self.d_daily:
                msg = msg+ "(?????????)"
            print(msg)
            
        # food
        if not self.enable_food:
            print("?????????????????????")
        else:
            time_rest = self.gap_food*60 - round(time.time()-self.t_food)
            if time_rest%60<10:
                print("?????????????????????: "+ str(time_rest//60) +':0' + str(time_rest%60))
            else:
                print("?????????????????????: "+ str(time_rest//60) +':' + str(time_rest%60))
        # auction
        if not self.enable_auction:
            print("?????????????????????")
        else:
            time_rest = self.gap_auction*60 - round(time.time()-self.t_auction)
            if time_rest%60<10:
                print("?????????????????????: "+ str(time_rest//60) +':0' + str(time_rest%60))
            else:
                print("?????????????????????: "+ str(time_rest//60) +':' + str(time_rest%60))
        if '??????' in MAP:
            print("?????????: ?????? "+ str(int(15*60+self.t_boss-time.time())) +"???")            
        # boss message
        if not self.check_boss:
            print('?????????????????????')
        if self.time_boss == None:
            print('??????????????????')
        else:
            hour_boss, min_boss = self.time_boss//60, self.time_boss%60
            if min_boss<10:
                msg = '????????????: ' + str(hour_boss) + ":0" +str(min_boss)
            else:
                msg = '????????????: ' + str(hour_boss) + ":" +str(min_boss)
            print(msg)
        if self.mode=='economic':
            print('???????????????: '+str(round(time.time()-self.t_eco))+' ???')

    ############
    ### Eyes ###
    ############
    def getWindowRect(self):
        x1, y1, x2, y2 = win32gui.GetWindowRect(self.hwnd)
        x1, y1, x2, y2 = x1+calibration[0], y1+calibration[1], x2+calibration[2], y2+calibration[3]
        w, h = x2 - x1, y2 - y1            
        return x1, y1, w, h
    # screenshot: delay=0.01 to prevent cpu overload
    def screenshot(self, delay=0.01):
        try:
            if self.title == 'Moonlight_Global':
                while win32gui.IsIconic(self.hwnd):
                    win32gui.ShowWindow(self.hwnd, 4)
                hwndDC = win32gui.GetWindowDC(self.hwnd)
                mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
                saveDC = mfcDC.CreateCompatibleDC()
                saveBitMap = win32ui.CreateBitmap()
                _, _, w, h = self.getWindowRect()            
                saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
                saveDC.SelectObject(saveBitMap)
                # Change the line below depending on whether you want the whole window or just the client area. 
                result = windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 3) #result = windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 0)
                bmpinfo = saveBitMap.GetInfo()
                bmpstr = saveBitMap.GetBitmapBits(True)

                img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

                win32gui.DeleteObject(saveBitMap.GetHandle())
                saveDC.DeleteDC()
                mfcDC.DeleteDC()
                win32gui.ReleaseDC(self.hwnd, hwndDC)
                self.img = np.asarray(img)
            else:
                while win32gui.IsIconic(self.hwnd):
                    win32gui.ShowWindow(self.hwnd, 4)
                hwindc = win32gui.GetWindowDC(self.hwnd)
                srcdc = win32ui.CreateDCFromHandle(hwindc)
                memdc = srcdc.CreateCompatibleDC()
                bmp = win32ui.CreateBitmap()
                _, _, w, h = self.getWindowRect()
                bmp.CreateCompatibleBitmap(srcdc, w, h)
                memdc.SelectObject(bmp)
                memdc.BitBlt((0 , 0), (w, h), srcdc, (0, 0), win32con.SRCCOPY)
                signedIntsArray = bmp.GetBitmapBits(True)
                img = frombuffer(signedIntsArray, uint8)
                img.shape = (h, w, 4)
                srcdc.DeleteDC()
                memdc.DeleteDC()
                win32gui.ReleaseDC(self.hwnd, hwindc)
                win32gui.DeleteObject(bmp.GetHandle())
                img = rgba2rgb(img)
                self.img = img
            return self.img
        except Exception as e:
            print('Error: winkey-screenshot')
            print(e)
            time.sleep(delay)
    def save_img(self, filename='img.png', shot=True, plot=True):
        if shot:
            self.screenshot()
        if plot:
            plt.imshow(self.img)
        cv2.imwrite(filename, self.img)
            
    def PixelExist(self, color_info, pos=0, show=-1, img=None, shot=1):
        # (c_x1, c_y1) ??????, (c_x2, c_y2) ??????, ??????
        # pixel: color
        # tol: tolerance
        # pos: 1 give positions, 0 give T/F
        # show: expand plot margin
        # img: None ??????
        c_x1, c_y1, c_x2, c_y2, pixel, tol = color_info
        try:
            if type(img)!=type(None): # if input img, current img = input img
                self.img = img
                shot=0
            if shot: # if not shot, use current img
                img = self.screenshot()
            
            h, w, _ = self.img.shape
            rgb = hex_to_rgb('#'+pixel[2:8])
            img_sub = self.img[int(c_y1*h):(int(c_y2*h)+1), int(c_x1*w):(int(c_x2*w)+1),]
            if show>=0:
                plt.imshow( self.img[(int(c_y1*h)-show):(int(c_y2*h)+show), (int(c_x1*w)-show):(int(c_x2*w)+show),] )
            if pos:
                posi = np.where((np.max(abs(img_sub-rgb),axis=2)<tol+5))
                return (c_x1+posi[1][0]/w, c_y1+posi[0][0]/h)
            else:
                return (np.max(abs(img_sub-rgb),axis=2)<tol+5).any()            
        except Exception as e:
            print(e)
            print('Error: winkey-PixelExist')
    def ImgExist(self, icon_info, pos=0, show=-1, img=None, value=0, shot=1, gray=0):
        # pos: return image position
        # show: plot the given region +margin = show
        # value: print the maximum res
        c_x1, c_y1, c_x2, c_y2, icon, thresh, x_icon, y_icon = icon_info
        try:
            if type(img)!=type(None): # if input img, current img = input img
                self.img = img
                shot=0
            if shot: # if not shot, use current img
                self.screenshot()
            if gray:
                self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
                icon = cv2.cvtColor(icon,cv2.COLOR_BGR2GRAY)

            _, _, w, h, = self.getWindowRect()
            sub_img = self.img[int(c_y1*h):int(c_y2*h), int(c_x1*w):int(c_x2*w),]            
            output = ImgSearch(icon, sub_img, threshold=thresh, x_scale = w/x_icon, y_scale = h/y_icon, pos=pos, value=value)
            if pos:
                output = (output[0], c_x1+output[1]/w, c_y1+output[2]/h)            
            if show>=0: # shot region
                plt.imshow(sub_img)
                # plt.imshow( self.img[(int(c_y1*h)-show):(int(c_y2*h)+show), (int(c_x1*w)-show):(int(c_x2*w)+show),] )
            return output
        except Exception as e:
            print(e)
            print('Error: winkey-ImgExist')
    #############
    ### Hands ###
    #############
    def checkerror(self):
        if self.is_WinActive():
            if self.checkusing == -1: # checusing=-1, ??????????????????
                print('???????????????')
                return
            elif self.checkusing==0: # checkusing=0, ??????????????????
                while self.is_WinActive():
                    print('????????????')
                    time.sleep(3)
                return
            elif self.checkusing==1: # checkusing=1, ????????????????????????????????????
                time_idle = getIdleTime()
                if time_idle<60:
                    return
                    # raise ValueError('???????????????, ???????????? '+str(int(time_idle))+' ???')                    
                else:
                    print('????????????????????????????????????')                    
                    def windowEnumerationHandler(hwnd, top_windows):
                        if  'python.exe' in win32gui.GetWindowText(hwnd):
                            top_windows.append(hwnd)
                    lst = []  # all open windows
                    win32gui.EnumWindows(windowEnumerationHandler, lst)
                    win32gui.SetForegroundWindow(lst[0])
                    
        _, _, w, h = self.getWindowRect()
        if w>0.9*win32api.GetSystemMetrics(0) or h>0.9*win32api.GetSystemMetrics(1):
            raise ValueError('???????????????')
        if self.ImgExist((0.226, 0.101, 0.855, 0.765, login_conflict, 0.95, 1400, 786)):
            login_anyway = False
            if login_anyway:
                self.myclick((0.501, 0.597))
            else:
                raise ValueError('????????????????????????')
                    
    def send(self, key, delay=1, msg=''):
        self.checkerror()
        try:
            if len(msg)>0:
                print(msg)
            if self.title == 'Moonlight_Global':
                self.win.send_keystrokes(key)
                t_click = time.time()
                time.sleep(delay)
            else:
                win32api.PostMessage(self.hwnd, win32con.WM_ACTIVATE, 0, 0)
                win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, key, win32api.MapVirtualKey(key, 0) << 16)
                time.sleep(0.05)
                win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, key, win32api.MapVirtualKey(key, 0) << 16)        
                t_click = time.time()
                time.sleep(delay)                
            return(t_click)
        except Exception as e:
            print(e)
            print('Error: winkey-send')            
    def send_char(self, char, delay=1):
        self.win.send_chars("????????????")
    def click(self, key, delay=1, msg='', press=0.01, pressmax=1, color_info=None, least=0.01, key2=None, press2=0, timemax=10):
        # press: Lbuttondown duration
        # color_info: Lbuttonup duration
        # press2: duration after drag to key2
        self.checkerror()
        try:
            if len(msg)>0:
                print(msg)
            if key==(0,0):
                return(time.time())
            _, _, w, h = self.getWindowRect()
            x, y = int(key[0]*w), int(key[1]*h)

            if self.title =='Moonlight_Global':
                old_pos = win32gui.GetCursorPos()
                while abs(win32api.GetKeyState(0x01))>1:
                    pass
                ok = windll.user32.BlockInput(True) #block input
                win32api.SetCursorPos(win32gui.ClientToScreen(self.hwnd, (x,y)))    
                win32gui.SendMessage(self.hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
                win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
                if key2==None:
                    if color_info==None:
                        time.sleep(press)
                    else:
                        t_least = t_start = time.time()
                        while not self.PixelExist(color_info) or time.time()-t_least<least:
                            if not self.PixelExist(color_info):
                                t_lease = time.time()
                            if time.time()-t_start>pressmax:
                                break
                            
                elif key2!=None: # drag
                    x2, y2 = int(key2[0]*w), int(key2[1]*h)
                    seg = 10
                    move = (x2-x)/seg, (y2-y)/seg
                    for i in range(0,seg):
                        x, y = x+move[0], y+move[1]
                        win32api.SetCursorPos(win32gui.ClientToScreen(self.hwnd, (int(x),int(y))))    
                        time.sleep(press)
                    time.sleep(press2)

                win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
                time.sleep(0.01)    
                win32api.SetCursorPos(old_pos)
                if abs(win32api.GetKeyState(0x11))>1:
                    pywinauto.keyboard.send_keys("{VK_CONTROL}")
                ok = windll.user32.BlockInput(False) #enable input
                
            else:
                lParam = win32api.MAKELONG(x, y)
                win32api.SendMessage(self.hwnd, win32con.WM_ACTIVATE, 2)
                win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
                if key2==None:
                    if color_info==None:
                        time.sleep(press)
                    else:
                        t_least = t_start = time.time()
                        while not self.PixelExist(color_info) or time.time()-t_least<least:
                            if not self.PixelExist(color_info):
                                t_lease = time.time()
                            if time.time()-t_start>pressmax:
                                break
                            
                elif key2!=None: # drag
                    x2, y2 = int(key2[0]*w), int(key2[1]*h)
                    seg = 10
                    move = (x2-x)/seg, (y2-y)/seg
                    for i in range(0,seg):
                        x, y = int(x+move[0]), int(y+move[1])
                        lParam = win32api.MAKELONG(x, y)
                        win32api.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0, lParam);
                        time.sleep(press)
                    time.sleep(press2)
                win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, None, lParam)
            t_click = time.time()
            time.sleep(delay)
            return(t_click)
        except Exception as e:
            print(e)
            ok = windll.user32.BlockInput(False) #enable input
            print('Error: winkey-click')        
        return
    def myclick(self, key=(0,0), delay=1, keywait=0.3, least=0.3, msg='', mode=0, color_info=None, timemax=10):
        # if key is string, used send method; else, use click
        # mode0: click
        # mode1: click intul appear
        # mode2: keep clicking until apear, click interval = delay
        # mode3: click until disappear
        # mode4: keep clicking until disappear, click interval = delay
        # if key==(0,0) and mode==1 or 3, this function is the same as waitpixel appear or diappear
        # possibly use *arg and **kwarg to generalize this function to 1. 'do_func once/n_times', 2. 'until condition_func appear/disappear' 3. with timemax
        if type(key)==str or type(key)==int: # if 
            point = self.send
        elif type(key)==tuple or type(key)==list:
            point = self.click
        else:
            raise ValueError('wrong key input')

        if mode==0: # click and wait delay
            point(key, delay=delay, msg=msg)
        else:
            if type(color_info)!=tuple and type(color_info)!=list:
                raise ValueError('color_infot cannot be '+str(type(color_info)))
            condition = 0
            t_lease = t_start = t_click = time.time()
            point(key, delay=keywait, msg=msg) # Always do while
            while not condition or time.time()-t_lease<least: # stop when condition and condition exist for least seconds
                if (mode==2 or mode==4) and not condition and time.time()-t_click>delay: # click until
                    t_click = point(key, delay=keywait, msg=msg)

                condition = self.PixelExist(color_info)
                if mode>2: # mode 3 and 4's condition is disappear
                    condition = not condition    
                if not condition: # t_least is the last time not fit condition
                    t_lease = time.time()    
                if time.time()-t_start>timemax: # if overtime
                    if mode<3:
                        print("???????????????")
                    else:
                        print("???????????????")
                    raise ValueError('????????????')
        return(time.time())
    ############################
    ### basic game functions ###
    ############################
    def login_func(self):
        if 'LDPlayer' in win32gui.GetClassName(self.hwnd0):
            factor = 1.15
        elif 'WindowOwnDCIcon' in win32gui.GetClassName(self.hwnd0):
            factor = 1
        login = self.ImgExist((0,0,1,1,gamelogo, 0.9, 1400*factor, 786*factor),pos=1)
        if login[0]<0.9:
            return

        self.login_num += 1
        self.resizeWindow()
        while self.ImgExist((0,0,1,1,gamelogo, 0.9, 1400*factor, 786*factor)):
            self.click((login[1], login[2]), delay = 2)
        self.click((0.5, 0.02), delay = 1)
        if self.PixelExist(color_redblood):
            return
        t_start=time.time()
        
        while not self.PixelExist((870/960, 80/540, 930/960, 309/540, '0xD7D928', 5)): # not find select character
            if time.time()-t_start>30*60: # if wait too long
                print('????????????')               
                self.shutdown()
                raise ValueError('????????????: ????????????')
            self.click((730/960, 297/540), 2)
        self.char = 1 
        if self.char==1:
            self.myclick((900/960, 95/540), delay=2, color_info=(870/960, 85/540, 930/960, 95/540, '0xD7D928', 0), msg='???????????? 1', mode=4) 
        if self.char==2:
            self.myclick((900/960, 171/540), delay=2, color_info=(870/960, 170/540, 930/960, 175/540, '0xD7D928', 0), msg='???????????? 2', mode=4) 
        self.waitloading()
        self.home_screen(timemax=120)
        print('????????????')

    def home_screen(self, checkmode=0, delay=1, keywait=0.3, timemax=10):
        # find red blood and fix white point
        hwnd_promotion = win32gui.FindWindowEx(None, None, None, 'Promotion')
        while hwnd_promotion!=0:
            time.sleep(5)
            lParam = win32api.MAKELONG(24, 653)
            win32api.SendMessage(hwnd_promotion, win32con.WM_ACTIVATE, 2)
            win32api.SendMessage(hwnd_promotion, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            time.sleep(0.05)
            win32gui.SendMessage(hwnd_promotion, win32con.WM_LBUTTONUP, None, lParam)
            time.sleep(2)
            hwnd_promotion = win32gui.FindWindowEx(None, None, None, 'Promotion')
        self.resizeWindow()

        if sum(self.img[10, 700,:] == self.img[20, 700,:])==3 and sum(self.img[10, 700,:] == self.img[10, 1380,:])==3: # ecomode
            if self.mode == 'economic':
                return
            else:
                self.myclick((0.56, 0.845), delay=delay, msg='??????????????????')
                self.screenshot()        
                while sum(self.img[10, 700,:] == self.img[20, 700,:])==3 and sum(self.img[10, 700,:] == self.img[10, 1380,:])==3: # ecomode
                    self.myclick((0.56, 0.845), delay=delay, msg='??????????????????')
                    time.sleep(2)
                    self.screenshot()
        
        if self.checkdead():
            if self.num_resurrect>0:
                self.num_resurrect -= 1
                self.resurrect(gap=self.gap_resurrect, num_friend=self.friend_basic)
            else:
                while self.checkdead():
                    print('??????????????????????????????')
                    time.sleep(10)
        
        
        # if loading
        while self.checkloading():
            print('loading')
            time.sleep(3)
                    
        # if in guild
        if self.leave_guild:
            in_guild = self.ImgExist((0.001, 0.162, 0.06, 0.9, back, 0.8, 1400, 786), pos=1)
            if in_guild[0]>0.85:
                # ????????????????????????
                self.myclick((0.938, 0.370), delay=delay, color_info=color_graycross, msg='????????????', mode=1) # ????????????
                self.myclick((0.77, 0.65), delay=delay)
                self.myclick((0.992, 0.031), delay=delay)
                
                time.sleep(2)
                if self.leave_pvp:
                    self.myclick((0.328,0.919), delay=delay)
                    if self.PixelExist( (0.4,0.6,0.4,0.6, '0x6B6152', 0) ) and self.PixelExist( (0.6,0.6,0.6,0.6, '0xD6DA29', 0)):
                        print('?????? pvp ??????')
                        self.myclick((0.548,0.618), delay=delay, color_info=(0.548,0.618,0.548,0.618,'0xD6DA29',5), mode=3)
                    else:
                        print('???????????? pvp ??????')
                        while not self.PixelExist(color_redblood):
                            self.myclick(key_back, delay=2, keywait=keywait, msg='??????', mode=2, color_info=color_redblood)
                        
                self.myclick((in_guild[1], in_guild[2]), delay=delay, msg='????????????', mode=1, color_info=(0.535, 0.599, 0.535, 0.599, '0xD6D727', 5))
                self.myclick((0.535, 0.599), delay=delay)
                self.waitloading()
                time.sleep(1)                
        openbox = (0.566,0.915,0.566,0.915,'0xD6DA29',5)
        #if self.PixelExist(openbox):
        #    self.myclick((0.566,0.915), delay=1, least=1, color_info=openbox, msg='??????', mode=4)

        
        t_start = time.time()
        while not self.checkhome_screen():
            if self.PixelExist((0.475, 0.6, 0.475, 0.6,'0x6B6152',5)):
                self.myclick((0.475, 0.6), delay=2, msg='??????')
            else:
                self.myclick(key_back, delay=2, msg='??????')                
            if time.time()-t_start>10:
                raise ValueError('????????????')

        # swith to page 1
        self.switch_page(page=1)        
        if self.check_boss and self.PixelExist( (0.414,0.205, 0.55, 0.310, '0x0000FF', 5) ): # Boss reborn message
            tz = pytz.timezone('Asia/Taipei')
            now = datetime.now(tz)
            self.save_img(filename=now.strftime("%Y")+'-'+now.strftime("%m")+'-'+now.strftime("%d")+'-'+now.strftime("%H")+now.strftime("%M")+'.png', shot=False, plot=False)

        if self.PixelExist((0.974, 0.571, 0.974, 0.571, '0xFFFFFF',0)) and self.PixelExist((0.934, 0.571, 0.934, 0.571, '0xD6D727',0)):
            self.myclick((0.974,0.571),delay=delay)
        
        print('?????????????????????')
        if checkmode:
            self.suitup()
            
        self.fight(1)
        # if self.mode=='economic':
        #     print('??????????????????')
        #     self.suitup()
        #     self.myclick((930/960, 30/540), delay=delay, msg='????????????', mode=2, color_info= (899/960, 480/540, 899/960, 480/540, '0xDBDD2C', 3), timemax=10)
        #     self.myclick((660/960, 500/540), delay=delay, msg='????????????', mode=4, color_info= (899/960, 480/540, 899/960, 480/540, '0xDBDD2C', 3), timemax=10)
        #     self.t_eco = time.time()
    def suitup(self):
        if (self.mode=='basic' or self.mode=='economic') and self.equip_basic+self.statue_basic+self.friend_basic> 0:
            self.change_equip(equip_target = self.equip_basic,
                              statue_target = self.statue_basic,
                              num_friend = self.friend_basic,
                              water_target = self.water_basic*10+20)
        elif self.mode=='raid' and self.equip_raid+self.statue_raid+self.friend_raid> 0:
            self.change_equip(equip_target = self.equip_raid,
                              statue_target = self.statue_raid,
                              num_friend = self.friend_raid,
                              water_target = self.water_raid*10+20)
        elif self.mode=='pvp' and self.equip_pvp+self.statue_pvp+self.friend_pvp> 0:
            self.change_equip(equip_target = self.equip_pvp,
                              statue_target = self.statue_pvp,
                              num_friend = self.friend_pvp,
                              water_target = 0)
        
            
    def change_equip(self, equip_target=0, statue_target=0, num_friend=0, water_target=0, fight=1, exe=0):
        if equip_target==0 and statue_target==0 and num_friend==0: # ???????????????
            return
        pts_equip = [(0.127, 0.826), (0.127, 0.752), (0.127, 0.678)]
        pts_statue = [(0.173, 0.826), (0.173, 0.752), (0.173, 0.678)]
        equip_current, statue_current = self.check_equip_and_statue()
        if self.ImgExist( (0.659,0.88, 0.7, 0.934, hpp, 0.9, 1400, 786)):
            water_current = 30
        else:
            water_current = 20
            
        if equip_current==equip_target and statue_current==statue_target and water_current==water_target:
            return        
        keep = True
        change = False
        while keep:
            # ??????????????????
            t_start=time.time()
            if equip_current!=equip_target and equip_target>0 and time.time()-t_start<3:
                if not self.PixelExist((0.144,0.833,0.144,0.833,'0xFFFFFF',0)) or not self.PixelExist((0.144,0.761,0.144,0.761,'0xFFFFFF',0)): # ?????????????????????
                    self.click((0.144,0.921),delay=0, color_info=(0.143,0.832,0.145,0.834,'0xFFFFFF',0))
            # ??????????????????
            t_start=time.time()
            if statue_current!=statue_target and statue_target>0 and time.time()-t_start<3:
                if not self.PixelExist((0.191,0.833,0.191,0.833,'0xFFFFFF',0)) or not self.PixelExist((0.191,0.761,0.191,0.761,'0xFFFFFF',0)): # ???????????????
                    self.click((0.191,0.921),delay=0, color_info=(0.190,0.832,0.192,0.834,'0xFFFFFF',0))                                
                    
            # ????????????
            if (equip_current!=equip_target and equip_target>0) or (statue_current!=statue_target and statue_target>0):
                print('????????????')
                if not change:
                    change = True
                    if fight:
                        self.fight(2) # semi
                    else:
                        self.fight(0)                        
                if (equip_current!=equip_target and equip_target>0):
                    self.myclick(pts_equip[equip_target-1], delay=0.1)
                if (statue_current!=statue_target and statue_target>0):
                    self.myclick(pts_statue[statue_target-1], delay=0.1)
                time.sleep(0.5)
                equip_current, statue_current = self.check_equip_and_statue()
            else:
                keep = False
                
        if water_target>0 and water_current!=water_target:
            change = True
            self.click((0.68,0.934),delay=0, color_info=(0.770,0.524,0.775,0.526,'0xFFFFFF',0))
            if water_target==20:
                self.myclick((0.705,0.62),delay=0.1)
            elif water_target==30:
                self.myclick((0.655,0.62),delay=0.1)        
        if change:
            if fight:
                self.fight(1) # auto mode
            else:
                self.fight(0)
        else: # did not change equip or statue
            return

        if num_friend>0 or exe:
            if self.title != 'Moonlight_Global':
                self.myclick(key_list, delay=delay, color_info=color_graycross, msg='????????????', mode=2)
            self.myclick(key_friend, delay=delay, color_info=color_graycross, msg='????????????', mode=2)
            num_friend -= 1
            row_friend, col_friend = num_friend//5, num_friend%5
            self.myclick( (0.679+col_friend*0.070, 0.346+row_friend*0.127) )
            if self.PixelExist((0.531, 0.921, 0.531, 0.921, '0xD6DA29',5)):
                self.myclick((0.531, 0.921), delay=delay, msg='????????????')
            elif self.PixelExist((0.531, 0.921, 0.531, 0.921, '0x6B6152',5)):
                print('????????????')
            else:
                print('??????????????????')
            self.home_screen()

    def eat_potion(self, check_sp=0, check_ep=0):
        A = check_sp and time.time()-self.t_sp>10*60
        B = check_ep and time.time()-self.t_ep>30*60
        if not A and not B:
            return
        
        self.myclick(key_bag, delay=delay, color_info=color_graycross, msg='????????????', mode=1)
        self.myclick((0.794, 0.109), color_info=(0.794,0.109,0.794,0.109,'0xFFFFFF',5), msg='?????????', mode=1)
        t_start=time.time()
        while A or B:
            if time.time()-t_start>20:
                print('???????????????')
                break
            val_sp, x_sp, y_sp = self.ImgExist((0.656, 0.137, 0.996, 0.715, sp, 0.1, 1400, 786), pos=1)    
            val_ep, x_ep, y_ep = self.ImgExist((0.656, 0.137, 0.996, 0.715, ep, 0.1, 1400, 786), pos=1)
            if check_sp and val_sp>0.97:
                if time.time()-self.t_sp<10*60:
                    print('????????????????????????')
                else:
                    self.myclick((x_sp, y_sp), delay=delay, color_info=(0.6, 0.885, 0.6, 0.885, '0xD6DA29',10), msg='??????????????????', mode=1)
                    self.myclick((0.6, 0.885),delay=2)
                    self.t_sp = time.time()
                    self.save_time()
            if check_ep and val_ep>0.97:
                if time.time()-self.t_ep<30*60:
                    print('??????????????????')
                else:
                    self.myclick((x_ep, y_ep), delay=delay, color_info=(0.6, 0.885, 0.6, 0.885, '0xD6DA29',10), msg='?????????????????????', mode=1)
                    self.myclick((0.6, 0.885),delay=2)
                    self.t_ep = time.time()
                    self.save_time()
            A = check_sp and time.time()-self.t_sp>10*60
            B = check_ep and time.time()-self.t_ep>30*60
            if not A and not B:
                break
            print('?????????')
            self.click(key=(0.7,0.7), key2=(0.7,0.5), press2=0.6)
        self.home_screen()
        return

    def fight(self, f_target=1):
        f_current = self.check_fight()
        if f_target==f_current:
            return
        elif f_target == 0: #
            self.myclick( (269/960, 495/540), delay=2, msg='????????????', mode=3, color_info=color_fight)
        elif f_target == 1:
            if f_current == 0:
                self.myclick( (269/960, 495/540), delay=2, msg='????????????', mode=1, color_info=color_fight)
            elif f_current == 2:
                self.click((0.28,0.913),delay=0, color_info=(0.293,0.831, 0.295, 0.833,'0xFFFFFF',10))
                self.click((0.28,0.828), delay=0.3, msg='??????????????????')
        elif f_target == 2:
            self.click((0.28,0.913),delay=0, color_info=(0.293,0.831, 0.295, 0.833,'0xFFFFFF',10))
            self.click((0.28,0.777),delay=0.3, msg='?????????????????????')

        self.fight(f_target) # recurssion       
        
    def fight_mode(self, mode='semi'):
        self.click((0.28,0.913),delay=0, color_info=(0.293,0.831, 0.295, 0.833,'0xFFFFFF',10))
        if 'semi' in mode:
            self.click((0.28,0.777),delay=0.1, msg='?????????????????????')
        else:
            self.click((0.28,0.828),delay=0.1, msg='??????????????????')
        
    def use_item(self, num, delay=1, msg=''):
        if num==0:
            return
        if len(msg)>0:
            msg= ': '+msg
        self.myclick( ((1090+77*num)/1600, 750/900), delay=delay, msg='???????????? '+str(num)+msg)
    def switch_page(self, page=0):
        if page==0:
            self.myclick(key_switch, delay=keywait, msg='???????????????')
        else:
            t_click, t_start = 0, time.time()
            stop = (page+self.ImgExist( (0.95,0.86, 0.99, 0.91, pageone, 0.9, 1400, 786))==2)
            while not stop:
                if time.time()-t_click>delay:
                    t_click = self.myclick(key_switch, delay=0.1, msg='?????????????????? '+str(page))
                stop = ( page+self.ImgExist( (0.95,0.86, 0.99, 0.91, pageone, 0.9, 1400, 786))==2)
                if time.time()-t_start>5:
                    raise ValueError('????????????')                        
        
    def decompose(self, delay=1):
        if self.exe<0:
            return
        condition_exe = max(self.exe, self.checkweight(), self.checkbagfull())
        if not condition_exe:
            return
        
        self.mode = 'basic'
        self.home_screen()
        
        print('????????????: ????????????')
        self.myclick(key_list, delay=delay, color_info=color_graycross, msg='????????????', mode=2)
        self.myclick((600/960, 100/540), delay=delay, color_info=(0.271, 0.151, 0.271, 0.151, '0xDEDEDE', 10), mode=1, timemax=10)
        self.myclick((780/960,  80/540), delay=delay, color_info=(0.860, 0.151, 0.860, 0.151, '0xDEDEDE', 10), mode=1, timemax=10)
        time.sleep(1)
            
        if self.PixelExist( (0.47, 0.665,0.489, 0.696, '0xFFFFFF',5) ):
            self.myclick((0.478, 0.681), delay=delay, msg='????????????')
            time.sleep(1)

        t_start = time.time()
        while not self.PixelExist((0.249, 0.356, 0.249, 0.356, '0x5B5B5B', 5)): # click until dim color
            if self.PixelExist((0.5,0.91,0.5,0.91,'0xD6DA29',10), shot=0):
                if self.title == 'Moonlight_Global':
                    self.myclick("{-}")
                else:
                    self.myclick((500/960, 493/540), delay=0.1, msg="??????")
            elif not self.PixelExist((0.860, 0.151, 0.860, 0.151, '0xDEDEDE', 0), shot=0):
                if self.title == 'Moonlight_Global':
                    self.myclick("{-}")
                    self.myclick("{-}")
                else:
                    self.myclick((0.600, 493/540), delay=0.05)
                    self.myclick((0.600, 493/540), delay=0.05)

            if time.time()-t_start>10:
                break

        self.home_screen()

    def sell(self, delay=1, remote=1):
        remote=1
        if self.exe<0:
            return
        condition_exe = max(self.exe, self.checkweight())
        if not condition_exe:
            return
        
        self.mode = 'basic'
        self.home_screen()
        
        self.myclick(key_bag, delay=delay, msg='????????????: ????????????', color_info=color_graycross, mode=2)
        if not self.PixelExist((0.892, 0.751,0.892, 0.751, "0xD3D727", 5)):
            print("??????????????????")
            self.home_screen()
            return
        self.myclick( (1497/1600, 686/900), delay=delay, color_info=color_blueconfirm, mode=1)
        self.myclick( (1000/1600, 550/900), delay=delay, color_info=color_blueconfirm, mode=3)
        time.sleep(delay)
        # sell 
        self.myclick( (168/960,  50/540), delay=delay, color_info=(0.307, 0.917,0.307, 0.917,'0xD6DA29',5), mode=1)
        self.myclick( (280/960, 495/540), delay=delay, color_info=(0.307, 0.917,0.307, 0.917,'0xD6DA29',5), mode=3)
        self.myclick(key_back, delay=delay)
    
    def storage(self, delay=1):
        if self.exe<0:
            return
        condition_exe = max(self.exe, self.checkweight())
        if not condition_exe:
            return
        
        self.mode = 'basic'
        self.home_screen()        
        if self.title != 'Moonlight_Global':
            self.myclick(key_list, delay=delay, color_info=color_graycross, msg='????????????', mode=2)
        self.myclick(key_friend, delay=delay, color_info=(0.281,0.156,0.281,0.156,'0xDEDEDE',5), msg='????????????: ????????????', mode=1)
        if not self.PixelExist( (0.422, 0.922,0.422, 0.922, "0x6B6152", 5) ):
            self.send(key_back, delay=delay, msg="????????????")
            return 
        if self.PixelExist( (0.539, 0.922, 0.539, 0.923, "0xD4D727", 5) ):
            self.myclick((0.818, 0.351), delay=delay, msg="??????????????????") # ?????????
            self.myclick((0.539, 0.922), delay=delay)
            
        self.myclick((0.422, 0.922), delay=delay, color_info=color_blueconfirm, mode=1, timemax=10)
        self.myclick((580/960, 325/540), delay=delay, color_info=(0.862, 0.925,0.862, 0.925,'0xD6DA29',5), mode=1, timemax=10)

        # save items
        self.myclick((800/960, 500/540), delay=delay, color_info=(0.971, 0.925,0.971, 0.925,'0xD6DA29',5), mode=1)
        self.myclick((900/960, 500/540), delay=delay)
        self.home_screen()

    def auction(self, delay=1):
        if self.exe<0:
            return
        if not self.enable_auction:
            return
        timemax=self.gap_auction*60
        condition_exe = max(self.exe, time.time()-self.t_auction>timemax)
        if not condition_exe:
            return

        self.mode = 'basic'
        self.home_screen()
        
        self.myclick(key_list, delay=delay, color_info=color_graycross, msg='????????????', mode=2)
        self.myclick((0.925, 0.629), delay=delay, color_info=(0.6, 0.17, 0.6, 0.17, '0xFFFFFF', 0), msg='?????????', mode=1, timemax=10)

        self.myclick((0.367, 0.950), delay=delay, color_info=(0.872,0.093,0.874,0.095,'0x6B6152',5), msg='????????????', mode=1)
        self.myclick((0.796, 0.903), delay=delay/4)
        self.myclick((0.855, 0.091), delay=delay/4)

        self.myclick((0.082, 0.410), delay=delay, color_info =(0.126,0.406,0.126,0.406,'0xD5D5D5',0), msg='????????????', mode=1)
        if not self.PixelExist((0.220,0.254,0.25,0.256,'0x6C6254',0)):
            self.myclick((0.082, 0.310), delay=delay, color_info =(0.126,0.310,0.126,0.310,'0xD5D5D5',0), msg='????????????', mode=1)
        self.myclick((0.889, 0.242), delay=delay, msg='??????')
        time.sleep(1)
        
        human_head = (0.679, 0.427, 0.681, 0.429, '0x6B6152', 0)
        y_upper = 0.335
        while True:
            gold = self.PixelExist(human_head)
            if gold: # 1st page
                lst = self.PixelExist((0.959, 0.333, 0.959, 0.91, '0xD5D728', 10))
            else: # 2nd page
                lst = self.PixelExist((0.959, y_upper, 0.959, 0.91, '0xD5D728', 10))
            if gold:
                if lst:
                    posi = self.PixelExist((0.959, 0.333, 0.959, 0.91, '0xD5D728', 10), pos=1)
                    self.myclick((posi[0], posi[1]), delay=delay, msg='??????')
                    if self.PixelExist( (0.575, 0.707, 0.575, 0.707, '0xD5D728', 10) ):
                        self.myclick((0.575, 0.707, 0.575, 0.707), delay=delay, color_info=human_head, msg='??????', mode=1)
                    else:
                        print('????????????')
                        break
                    # ????????????
                    if self.PixelExist( (posi[0]-0.01, posi[1]-0.01, posi[0]+0.01, posi[1]+0.01, '0xD5D728', 3) ):
                        print('????????????20?????????')
                        break                    
                else:
                    self.myclick((0.171, 0.252, 0.171, 0.252), color_info=human_head, delay=delay, msg='??????', mode=3)
                    y_upper = y_upper + 0.142
            else: # no gold
                if lst:
                    posi = self.PixelExist((0.959, y_upper, 0.959, 0.91, '0xD5D728', 10), pos=1)
                    self.myclick((posi[0], posi[1]), delay=delay, color_info=human_head, msg='????????????', mode=1)
                else:
                    break    
        self.home_screen(delay=delay)
        self.t_auction = time.time()    
        self.save_time()
        
    ###############################
    ### advanced game functions ###
    ###############################
    def resurrect(self, gap, num_friend):
        t_start = time.time()
        while time.time()-t_start<gap:
            print('????????????'+str(int(t_start+gap-time.time())))
            time.sleep(1)
        self.myclick((475/960, 270/540), delay=delay, msg='????????????')                
        while not self.PixelExist(color_fight):
            self.fight(1)

        if num_friend>0:
            if self.title != 'Moonlight_Global':
                self.myclick(key_list, delay=delay, color_info=color_graycross, msg='????????????', mode=2)        
            self.myclick(key_friend, delay=delay, color_info=color_graycross, msg='????????????', mode=2)
            num_friend -= 1
            row_friend, col_friend = num_friend//5, num_friend%5
            self.myclick( (0.679+col_friend*0.070, 0.346+row_friend*0.127) )
            if self.PixelExist((0.531, 0.921, 0.531, 0.921, '0xD6DA29',5)):
                self.myclick((0.531, 0.921), delay=delay, msg='????????????')
            elif self.PixelExist((0.531, 0.921, 0.531, 0.921, '0x6B6152',5)):
                print('????????????')
            else:
                print('??????????????????')
            self.myclick(key_back, delay=1, msg='??????')
        return
    
    def debuff(self, icon, key, icon_reso, name):
        if type(key)!=str:
            return
        delay=2
        _, _, w, h, = self.getWindowRect()
        x1, y1, x2, y2 = int(10/1919*w), int(130/1015*h), int(240/1919*w), int(160/1015*h)  ## debuff region
        self.screenshot()
        img_sub = self.img[y1:y2, x1:x2,]
        debuff = ImgSearch(icon, img_sub, threshold=0.8, x_scale = w/icon_reso[0], y_scale = h/icon_reso[1])
        if not debuff:
            print("???"+name+"??????")
            return 

        print("??????"+name+"??????")
        self.switch_page(page=2)
        while debuff:
            t_click = time.time()
            self.myclick(key, delay=0.1, msg='??????')        
            while time.time()-t_click<delay and debuff:
                self.screenshot()
                img_sub = self.img[y1:y2, x1:x2,]
                debuff = ImgSearch(icon, img_sub, threshold=0.8, x_scale = w/icon_reso[0], y_scale = h/icon_reso[1])
        print("??????"+name)
        
    def food(self, exe=0):
        key = self.key_food
        if exe<0 or type(key)!=str:
            return
        if not self.enable_food:
            return
        timemax=self.gap_food*60
        if time.time()-self.t_food<timemax and exe==0:
            return
        self.myclick(key_info, delay=delay, color_info=color_redblood, mode=4, msg='????????????buff')
        time.sleep(0.5)
        if not self.PixelExist((0.251, 0.093, 0.251, 0.093, '0xFFFFFF', 0)):
            self.myclick((0.251, 0.093), delay=delay, color_info=(0.251, 0.093, 0.251, 0.093, '0xFFFFFF', 0), mode=2)
        if not self.PixelExist((0.040, 0.387, 0.040, 0.387, '0xFFFFFF', 0)):
            self.myclick((0.040, 0.387), delay=delay, color_info=(0.040, 0.387, 0.040, 0.387, '0xFFFFFF', 0), mode=2)

        self.click(key=(0.25, 0.16), key2=(0.26, 0.95)) # ?????????        
        food_status = False

        t_start = time.time()
        while not food_status and time.time()-t_start < 4:
            food_status = self.ImgExist(icon_info=(0.079, 0.132,0.351, 0.98,food_effect, 0.75, 1473,827))
            
        if food_status:
            print('??????buff??????')
            self.t_food = time.time()-timemax+60*5 # check food after 5 minute
        else:
            print('????????????buff')
            self.switch_page(page=1)
            self.myclick(key, delay=delay, mode=0, msg='?????????buff')
            self.t_food = time.time()
        self.save_time()

        self.home_screen()
   
    def leashboss(self, leash = 0):
        key_h, key_v = '{D}', '{W}'  # horizontal and vertical keys
        boss = self.BossExist() # this print boss' position
        if boss!=(0,0):
            dx, dy = boss[0]-0.5, boss[1]-0.5
            dist = np.linalg.norm((dx, dy))
            if dist<0.2 and leash:
                print('??????BOSS!')
                if dx>0:
                    key_h = '{A}'
                if dy>0:
                    key_v = '{W}'
                if np.random.rand()>1/3: # 2/3 probability change key
                    self.key_pre = 1-self.key_pre
                    
                if self.key_pre==0:
                    self.myclick(key_h, delay=0.4)
                    self.myclick((0.711,0.547), delay=0.1)
                else:
                    self.myclick(key_v, delay=0.4)
                    self.myclick((0.711,0.547), delay=0.1)
                
                
    def FightBoss(self, BOSS, tele1=1, tele2=1, delay=1):
        # tele: 0 ??????, 1 ????????????, 2 ????????????
        # tele1: ?????????
        # tele2: ?????????
        # self.fighboss 1: go boss, 2: go farm
        if '??????' not in MAP or BOSS not in MAP:
            return
        if time.time()-self.t_boss < 15*60+0:
            return

        t_hunt = self.hour_guild*60+self.min_guild
        if clock2()>t_hunt and clock2()<t_hunt+125:
            print('??????????????????')
            return

        lower = self.hour_start_pvp*60 + self.min_start_pvp
        upper = self.hour_end_pvp*60 + self.min_end_pvp
        if (clock2()>lower and clock2()<upper) or not self.enable_pvp:
            print('pvp????????????')
            return
        print("????????????????????? !")

        boss_born = self.map(TO=BOSS,FROM='??????',tele=tele1, checkboss=True)  # go method = tele1
        if not boss_born:
            self.t_boss = time.time()-600 # ???????????????10??????
            self.save_time()
        else:
            self.fight(2)
            self.click((0.28,0.913),delay=0, color_info=(0.293,0.831, 0.295, 0.833,'0xFFFFFF',10)) # ????????????auto
            self.map(TO=BOSS, FROM=BOSS, checkboss=False)  # go method = tele1
            self.summon_friend(self.friend_raid)
            t_loop = t_start = time.time()
            self.checkusing = 0 # ?????????????????????
            self.boss_status = 0
            while time.time()-t_start<5*60: # ?????????6??????
                if not self.checkhome_screen():
                    self.myclick(key_back, delay=0.5, msg='???????????????')
                self.BossExist()
                if self.boss_status==0:
                    print('???????????????! ')                    
                elif self.boss_status == 1:
                    self.boss_status = 0
                    print("?????????! ?????????")
                    self.t_boss = time.time()
                    self.save_time()
                    break
                elif self.boss_status==self.boss_status_max:
                    print('????????? / ?????????!')
                    if self.PixelExist((0.293,0.831, 0.295, 0.833,'0xFFFFFF',10)): # ????????????????????????
                        self.click((0.28,0.828), delay=0.3, msg='??????????????????')
                    else:
                        self.fight(1)
                else: # self.boss_status=1 ~~ self.boss_status_max-1
                    print('???????????????: '+str(self.boss_status) +'???')
                    t_loop = time.time()                    

                while time.time()-t_loop<1:
                    pass
        self.summon_friend(self.friend_basic)
        self.checkusing = 1
        self.map(TO='??????',FROM=BOSS, tele=tele2, checkboss=False)
        self.fight(1)        

    def map(self, TO, FROM=None, delay=1, tele=0, checkboss=False):
        # tele=0: ???????????????????????????
        # tele=1: ???????????????
        # tele=2: ???????????????
        
        # TO format: (fx, fy), or "????????????" (must in MAP.key())
        if type(TO)!=type(' '):       # ???????????????
            fx_to, fy_to = TO
            subregion_to, region_to = 0, 0
            tele = 0
        elif TO in MAP.keys():
            tx_to, ty_to, fx_to, fy_to, subregion_to, region_to = MAP[TO]
        else:
            print('????????????')

        # FROM format: "????????????" (must in MAP.key())
        if FROM in MAP.keys():
            tx_from, ty_from, fx_from, fy_from, subregion_from, region_from = MAP[FROM]
        elif FROM == None:
            subregion_from, region_from = subregion_to, region_to
            
        ### open target map
        self.home_screen()
        while tele>0 and not self.checkloading():
            if tele==1:
                self.myclick( (900/960, 200/540), delay=delay, color_info=color_graycross, msg='????????????', mode=1)
                if subregion_from!=subregion_to or region_from!=region_to: # different subregion
                    self.myclick((0.97, 0.91), delay=delay, msg='???????????????', color_info=(0.96,0.93,0.97,0.94,'0x6B6152', 5),mode=4) # map
                    x, y = REGION[region_to]
                    self.myclick((x, y), delay=delay, msg=region_to, color_info=(0.96,0.93,0.97,0.94,'0x6B6152', 5),mode=2) # map
                    x, y = SUBREGION[subregion_to]
                    self.myclick((x, y), delay=delay, msg=subregion_to, color_info=(0.780,0.93,0.79,0.94,'0x6B6152',5),mode=4) # map
                    
                self.myclick((tx_to, ty_to), delay=1)
                self.myclick((tx_to, ty_to+0.04), delay=1, color_info=color_blueconfirm, mode=2, msg='????????????')                
                self.myclick((0.56, 0.59), delay=1, color_info=color_blueconfirm, mode=4, msg='????????????')
            elif tele==2:
                # need to define key_scroll                    
                self.home_screen()
                self.fight(2) # switch to semi
                self.switch_page(2)
                key_scroll = '{F3}'
                self.myclick(key_scroll, delay=3, color_info=color_redblood, msg='????????????', mode=4)
            time.sleep(1)
        
        if self.checkloading():
            self.waitloading()

        self.myclick((900/960, 200/540), delay=delay, color_info=color_graycross, msg='????????????', mode=2)
        self.myclick((fx_to, fy_to), delay=delay, msg='???????????????')

        if checkboss and subregion_to!=subregion_from: # ??????????????????: ?????????????????????
            t_start = time.time()
            while time.time()-t_start<5: # Boss reborn message
                if self.PixelExist((0.414,0.205, 0.55, 0.310, '0x0000FF', 5)):
                    boss = 1
                    break
                else:
                    boss = 0
            if boss:
                print('????????????!')
            else:
                print('???????????????zz')
        else: # ??????????????????: ????????????????????????
            print('??????????????????!')        
            boss=1
        self.home_screen(delay=delay)
        return boss
    #################################################
    ################ under construction #############
    #################################################
    def teamup(self, delay=1):
        if self.team_accept and self.PixelExist((0.225, 0.420, 0.229, 0.424, '0xD6DA29', 5)):
            self.myclick((0.227,0.422), delay=delay, color_info=(0.225, 0.420, 0.229, 0.424, '0xD6DA29', 5), mode=3, msg='????????????')

        if not self.team_add or not self.PixelExist((0.616, 0.94, 0.64, 0.993,'0x39FA4C',10)): # light green color
            return
        self.myclick((0.441,0.934), delay=delay, msg='???????????????')
        self.myclick((0.036,0.733), delay=delay)

        ## ???????????????
        cy = 0.881
        while cy>0.067:
            value, x, y = self.ImgExist((0.071,cy,0.296, cy+0.05,password_teamup2,0.93,1400,786),gray=1,pos=1)
            if value>0.6 and self.PixelExist( (0.080, y-0.07, 0.085, y-0.03, '0x0000FF',5)):
                break
            cy = cy-0.025
        if cy<0.067:
            print('????????????')
            self.myclick((0.037, 0.485), delay=delay)
        else:  
            self.myclick( (0.085, cy), delay=delay, msg='??????????????????' )        

            # ????????????
            self.myclick((0.095, 0.861), delay=delay, msg='????????????')
            self.myclick((0.248, 0.168), delay=delay)

        # ????????????
        self.myclick((0.233,0.959), delay=0.5, msg='OK') # ????????????
        self.myclick((0.499,0.092), delay=0.5) # ????????????
        self.myclick((0.394,0.538), delay=0.5) # ok
        self.myclick((0.335,0.098), delay=0.5) # ??????????????????

        # ??????
        self.home_screen()
    def guild_hunt(self, delay=1):
        if not self.enable_hunt:
            return
        t_now, t_hunt = clock2(), self.hour_guild*60+self.min_guild

        if t_now < t_hunt or (t_now > t_hunt+1): # relate this to d_hunt
            return
        if self.enter_hunt==clock2('day'):
            return
        print("?????????! hunt!!")
        self.mode='basic'
        self.home_screen()
                
        self.fight(2)
        self.myclick(key_list, delay=delay, color_info=color_graycross, msg='????????????', mode=2)
        self.myclick((0.614,0.627), delay=delay, color_info=color_graycross2, msg='??????', mode=3)

        ## ??????????????????
        t_temp = time.time()
        while not self.checkloading():
            t_start = time.time()
            while self.PixelExist(color_redblood) and time.time()-t_start < 5: # ??????bug???????????????
                pass
            if time.time()-t_start>=5:
                self.myclick(key_list, delay=delay, color_info=color_graycross, msg='????????????', mode=2)
                self.myclick((0.614,0.627), delay=delay, color_info=color_graycross2, msg='??????', mode=3)

            if self.PixelExist(color_graycross):
                self.myclick((0.221,0.873), delay=delay, msg='????????????')
                self.myclick((0.540,0.595), delay=2, msg='??????')

            if time.time()-t_temp>120:
                raise ValueError('????????????')
        self.waitloading()

        
        ## ?????????????????????
        self.myclick((0.938, 0.370), delay=delay, color_info=color_graycross, msg='???????????????', mode=1) # ????????????
        self.myclick((0.718, 0.517), delay=delay, color_info=(0.718-0.05, 0.517-0.05, 0.718+0.05, 0.517+0.05, '0x4856EE', 5), mode=1)
        self.myclick((0.992, 0.031), delay=delay)
        time.sleep(5)

        ## ??????PVP
        if self.enter_pvp:
            self.myclick((0.328,0.919), delay=delay)
            if self.PixelExist( (0.4,0.685,0.4,0.685, '0x6B6152', 0) ) and self.PixelExist( (0.6,0.685,0.6,0.685, '0xD6DA29', 2)):
                print('?????? pvp ??????')
                self.myclick((0.539,0.662), delay=delay, color_info=(0.539,0.662,0.539,0.662,'0xD6DA29',5), mode=3)
            else:
                print('???????????? pvp ??????')
                while not self.PixelExist(color_redblood):
                    self.myclick(key_back, delay=2, keywait=keywait, msg='??????', mode=2, color_info=color_redblood)
            
        ## ??????
        self.myclick((0.515, 0.586), delay=delay)
        
        if self.PixelExist((0.671,0.808,0.675,0.812,'0xD6DA29',5)):
            self.myclick((0.673, 0.810), delay=delay, msg='????????????')
        else:
            print('????????????????????????')
            self.myclick(key_back, delay=2, keywait=keywait, msg='??????', mode=2, color_info=color_redblood)
            self.home_screen()
            return

        ## ???loading 
        self.waitloading()

        ## ???????????????        
        self.myclick((0.938, 0.370), delay=delay, color_info=color_graycross, msg='???????????????', mode=1) # ????????????
        while True:
            self.myclick( (self.x_guild, self.y_guild), delay=delay) # ??????fx, fy            
            if  self.PixelExist((self.x_guild-0.05, self.y_guild-0.05, self.x_guild+0.05, self.y_guild+0.05, '0x4856EE', 5)):
                break
            else:
                self.x_guild, self.y_guild = self.x_guild+0.01, self.y_guild+0.01
        self.fight(1)
        self.enter_hunt = clock2('day')
        
    def raid_boss(self, x_boss, y_boss):
        # ???????????????????????????????????????
        boss_blood = (0.655, 0.103, 0.660, 0.107, '0x38C4FF', 10) # ??????x3~x1
        boss_bloodnumber = (0.46, 0.095, 0.49, 0.1, '0xFFFFFF', 20)
        boss_debuff = (0.40, 0.12, 0.45, 0.15, '0x6550E7',0)
        boss_health = 2 #0: dead, 1: on, 2: nor appear
        
        self.checkusing = 0 # ?????????????????????
        self.mode = 'raid'

        # exe=1: change friend and water
        self.change_equip(equip_target=self.equip_raid,
                          statue_target=self.statue_raid,
                          num_friend=self.friend_raid,
                          water_target=water_raid*10+20, fight=0, exe=1) # True=30, False=20
        ct = 0
        keep = True
        t_click = time.time()
        key_press = 0
        while keep:
            try:
                t_start = time.time()
                while not self.checkhome_screen(): # ?????????screenshot 
                    # ?????????????????????self.gap_resurrect_pvp????????????
                    if self.checkdead(shot=0):
                        print('????????????')
                        self.resurrect(gap=self.gap_resurrect_raid, num_friend=self.friend_raid)
                    # ??????????????????ESC
                    if self.PixelExist((0.475, 0.6, 0.475, 0.6,'0x6B6152',5)):
                        self.myclick((0.475, 0.6), delay=2, msg='??????')
                    else:
                        self.myclick(key_back, delay=2, msg='??????')
                    if time.time()-t_start>15:
                        print('?????????????????????????????????')
                        break

                # ??????????????????
                E1 = self.PixelExist(boss_blood, shot=0) # ??????X1~X3
                E2 = self.PixelExist(boss_debuff, shot=0) # 
                
                # ????????????
                # step1: not E1 and  health=2
                # step2: E1 and E2 and health==2, then change to E1 and E2 and health==1 ?????????
                # setp3: E1 and E2 and health==1, wait for E1 and not E2 and health==1
                # step4:             
                if not E1 and boss_health==2:
                    # ????????????
                    ct+=1            
                    print('?????????????????????')
                    if ct==1:
                        self.map((x_boss, y_boss), checkboss=False)
                        self.eat_potion(check_sp=self.sp_raid, check_ep=0)
                    elif not self.PixelExist((0.495, 0.790, 0.505, 0.800, '0xFFFFFF',5)):
                        if time.time()-t_click>10:
                            if key_press:
                                t_click = self.myclick(self.key_left, delay=0.1, msg='??????')
                            else:
                                t_click = self.myclick(self.key_right, delay=0.1, msg='??????')
                            key_press = 1-key_press
                            
                elif E1 and E2:
                    # ?????????
                    if boss_health == 2:
                        print('???????????????!')
                        self.fight(1)
                        time.sleep(10)
                    else:
                        print('??????????????????!')
                    boss_health = 1
                elif E1 and not E2: # ?????????????????????????????????????????????????????????????????????
                    if boss_health==1:
                        print('???????????????') # 
                        boss_health = 0
                        time.sleep(5)
                        # ???????????????????????????
                    elif boss_health==0:
                        print('??????????????????! ')
                        keep = False
                time.sleep(1)
            except:
                print('????????????????????????')         
            
        # ??????
        self.myclick((0.874, 0.575), delay=0.5, msg='????????????')
        self.myclick((0.874, 0.575), delay=0.5, msg='????????????')
        self.myclick((0.874, 0.575), delay=0.5, msg='????????????') 
        self.myclick((0.535, 0.598), delay=delay, msg='??????') # blue finish:
        self.checkusing = 1
        self.mode = 'basic'        
        self.waitloading()
        
    def normal_raid(self, delay=1):
        if self.level_raid==0:
            return
        if not self.enable_raid:
            return
        if self.level_raid==290:
            return

        t_now = clock2()
        enter = 0        
        for i in range(0,6):
            if getattr(self, 'raid'+str(i+1)) and self.raid_start[i]>t_now and t_now>=self.raid_start[i]-self.early_raid:
                enter = 1
                break
        if not enter:
            return

        self.mode='raid'
        self.home_screen()
        
        self.myclick(key_list, delay=delay, color_info=color_graycross, msg='????????????', mode=2)
        # because timemax = 3, it okay to apply this function during guild_hunt
        self.myclick((0.686, 0.346), delay=delay, color_info=(0.5,0.057,0.5,0.057,'0xFFFFFF',0), msg='??????', mode=1, timemax=2*delay)
        for i in range(0,6):
            self.click(key=(0.1, 0.98), key2=(0.1, 0.02)) # ?????????.
            if self.title=="Moonlight_Global" and i>1:
                break
        
        if self.level_raid==219:
            self.click(key=(0.1, 0.4), press=0.3, key2=(0.1, 0.65), press2=0.5)
            h = 1
            name, fx, fy = '????????????????????????', 0.798, 0.504
        elif self.level_raid==210:
            h = 1
            name, fx, fy = '??????????????????', 0.828, 0.453
        elif self.level_raid==229:
            h = 2
            name, fx, fy = '????????????????????????', 0.828, 0.453
        elif self.level_raid==280:
            h = 3
            name, fx, fy = '??????????????????', 0.802, 0.498
        elif self.level_raid==295:
            h = 4
            name, fx, fy = '????????????????????????', 0.802, 0.498
        elif self.level_raid==290:
            h = 5
            name, fx, fy = '???????????????', 0.792, 0.406
        elif self.level_raid==305:
            h = 6
            name, fx, fy = '?????????????????????', 0.792, 0.406

        self.myclick( (0.1, 0.097+0.144*h), delay=delay, msg='??????'+name)

        # ?????????????????????
        if not self.PixelExist((0.739, 0.897, 0.741, 0.899, '0xD6DA29',5)):
            print('????????????')
            return
        else:
            self.myclick( (0.741,0.896), delay=delay, msg='????????????')
            if self.PixelExist((0.57, 0.664, 0.57, 0.664, '0xD6DA29',5)): # ???????????????????????????
                if self.ticket_raid:
                    self.myclick((0.57,0.664), delay=delay, msg='??????')
                else:
                    return
        if self.PixelExist(color_graycross): # ??????????
            raise ValueError('error-????????????')        
        self.waitloading()
        self.raid_boss(x_boss=fx, y_boss=fy)
        self.mode = 'basic'
        return

    def guild_raid(self, just_check=True):
        if clock2()<20*60+20:
            return
        if time.time()-self.t_guild_raid>2*60:
            print('?????????????????? '+str(int(120+self.t_guild_raid-time.time()))+'???')
            return

        
        name, fx, fy = '?????????????????????', 0, 0
        self.myclick(key_list, delay=delay, color_info=color_graycross, msg='????????????', mode=2)
        self.myclick((0.614, 0.627), delay=delay, color_info=color_graycross2, msg='??????', mode=3)
        self.myclick((0.696, 0.191), delay=delay, color_info=(0.696, 0.191, 0.696, 0.191, '0xDEDEDE', 0), msg='????????????', mode=1)
        self.myclick((0.445, 0.275), delay=delay, color_info=(0.445, 0.275, 0.445, 0.275, '0xDEDEDE', 0), msg='????????????', mode=1)
        self.myclick((0.171, 0.440), delay=delay, color_info=(0.171, 0.440, 0.171, 0.440, '0xDEDEDE', 0), msg=name, mode=1)
        
        if self.PixelExist((0.721, 0.897, 0.721, 0.897, '0xDCDC89', 0)):
            print('?????????????????????')
            self.t_guild_raid = time.time()
            self.home_screen()
            return
        else:
            if just_check:
                self.home_screen()
                self.fight(2)
                #self.guild_raid(just_check=False)
                guild_raid(just_check=False)
                return
            else:
                self.myclick((0.721, 0.897), delay=2)
                self.myclick((0,0), delay=2, msg='??????')
                self.waitloading()
                
        self.raid_boss(x_boss=fx, y_boss=fy)
        return
    
    def daily_raid(self, delay=1):
        if not self.enable_daily:
            return
        tz = pytz.timezone('Asia/Taipei')

        d_now, h_now = clock2('day'), clock2()
        if h_now < 5*60:
            d_now -= 1
        if d_now<=self.d_daily:
            return
        if clock2()<self.hour_daily*60 + self.min_daily:
            return

        self.mode = 'basic'
        self.home_screen()
        
        ######## new test ###########
        #self.coinstore_gift_explore()
        self.get_reward() # 
        self.coinstore(acc=1)
        #############################
        
        self.home_screen()
        print('??????????????????')
        self.fight(2)
        self.myclick(key_list, delay=delay, color_info=color_graycross, msg='????????????', mode=2)
        self.myclick((0.615,0.333), delay=delay, color_info=color_graycross2, msg='??????', mode=3)
        # if red point, then complete it
        # it not red point, daily raid has been completed today
        # if self.PixelExist((0.022,0.154,0.022,0.154,'0x0000FF',5)):
        if self.PixelExist((0.324,0.154,0.324,0.154,'0x0000FF',5)):
            # ????????????
            self.myclick((0.324, 0.169), delay=delay, msg='????????????')

            level = 8
            self.myclick((0.158, 0.150+0.105*level), delay=delay, color_info=(0.158, 0.150+0.105*level, 0.158, 0.150+0.105*level, '0xDEDEDE',0), mode=1)
            while not self.PixelExist((0.732, 0.826, 0.732, 0.826, '0xD5D728',5)):
                level -= 1
                self.myclick((0.158, 0.150+0.105*level), delay=delay, color_info=(0.158, 0.150+0.105*level, 0.158, 0.150+0.105*level, '0xDEDEDE',0), mode=1)

            self.myclick((0.791, 0.826), color_info=color_graycross,delay=delay, msg='????????????: ??????'+str(level),mode=4)
            self.waitloading()
            self.fight(1)

            least = 0.3
            t_least = time.time()
            print('??????????????????')                
            while time.time()-t_least<least:
                if not self.PixelExist((0.530, 0.665, 0.535, 0.670, '0x6B6152',5)):
                    t_least = time.time()
            self.myclick((0.531, 0.669), delay=delay, msg='??????????????????! ????????????')
            self.waitloading()

        # ????????????????????????
        self.home_screen()
        self.d_daily = clock2('day')
        self.save_time()

    def coinstore(self, acc=1):
        ## ????????????
        self.myclick(key_mall, delay=1, color_info=color_graycross, mode=1, msg='????????????')
        self.myclick((0.816, 0.155), delay=1, color_info=(0.81,0.15,0.82, 0.16,'0xDEDEDE', 5),mode=1, msg='????????????')
            
        if acc==1:
            pages = range(0,4)
        else:
            pages = range(1,2)

        items = os.listdir('figures/item_daily')

        threshold = 0.8
        if self.title=='Moonlight_Global':
            threshold = 0.92
        for i in pages:
            self.myclick((0.15,0.257+i*0.094),delay=1,color_info=(0.145,0.25+i*0.094,0.26+i*0.094,0.155,'0xDEDEDE',5),msg='?????????')

            j=0
            while j < len(items):
                item = items[j]
                if 'acc'+str(acc) in item:
                    item = cv2.imread('figures//item_daily//'+str(item))
                    item = cv2.cvtColor(item, cv2.COLOR_RGB2BGR)
                    img_pos = self.ImgExist((0,0,1,1,item, 0.1,1400,786),pos=1)
                    if img_pos[0]>threshold:
                        self.myclick( (img_pos[1],img_pos[2]), delay=1, color_info=(0.67,0.80,0.68,0.81,'0xD6DA28',5), mode=1,msg='????????????')
                        if self.PixelExist((0.78,0.65,0.79,0.66,'0x6B6152',0.5)):
                            self.myclick((0.785,0.65),delay=0.5)
                        self.myclick((0.678,0.805),delay=0.5)
                        while self.ImgExist((0,0,1,1,item, threshold,1400,786)): # ??????????????????
                            print(1)
                            time.sleep(1)
                            pass
                        items.pop(i)
                    else:
                        j += 1
                        
        self.myclick((0.538, 0.155), delay=1, color_info=(0.538,0.15,0.538, 0.16,'0xDEDEDE', 5),mode=1, msg='??????')
        item = cv2.imread('figures//item_daily//acc1_17.png')
        item = cv2.cvtColor(item, cv2.COLOR_RGB2BGR)
        img_pos = self.ImgExist((0,0,1,1,item, 0.1,1400,786),pos=1)
        if img_pos[0]>0.90:
            self.myclick((0.588, 0.812), delay=1, color_info=(0.67,0.80,0.68,0.81,'0xD6DA28',5), mode=1,msg='????????????')
            self.myclick((0.678,0.805),delay=0.5)
        self.home_screen()
            

    def coinstore_gift_explore(self):
        if not hasattr(self, 'accounts') or not hasattr(self, 'lst_friends'):
            return
        self.checkusing = 0 # ?????????????????????
        # 1. logout, then login account
        for acc in self.accounts:    
            ## logout
            self.home_screen()
            ## ???????????????????????????2
            if acc==2:
                self.fight(2)
            self.myclick(key_list, delay=delay, color_info=color_graycross, msg='????????????', mode=2)
            while self.PixelExist((0.98,0.91,0.99,0.92,'0xD6DA29',0)):
                self.myclick((0.982,0.916), delay=1, msg='??????')
            
            ## login
            while not self.PixelExist((0.93,0.051+0.121*1,0.94,0.051+0.121*4, '0xD6D826',0)):
                pass
            for i in range(0,4):
                self.myclick((0.93,0.051+0.121*acc),delay=1, msg='????????????: '+str(acc))
            self.waitloading(timemax=90)
            
            ## wait daily gift
            keep = True
            self.screenshot()
            for j in range(0,4):
                for i in range(0,7):
                    keep = self.PixelExist( (0.332+i*0.088, 0.390+j*0.135, 0.336+i*0.088, 0.394+j*0.135, '0xD5D827',0), shot=0)
                    if not keep:
                        break
                if not keep:
                    break
            self.myclick( (0.334+i*0.088, 0.392+j*0.135), delay=0.5, msg='??????????????????')                
            self.home_screen()

            ## ??????????????????????????????????????????
            if acc==1:
                self.fight(1)
                
            ## ????????????
            self.myclick('{U}', delay=1, color_info=color_graycross, mode=1, msg='????????????')
            self.myclick((0.816, 0.155), delay=1, color_info=(0.81,0.15,0.82, 0.16,'0xDEDEDE', 5),mode=1, msg='????????????')
            
            if acc==1:
                pages = range(0,6)
            else:
                pages = range(1,2)
            for i in pages:
                self.myclick((0.15,0.257+i*0.094),delay=1,color_info=(0.145,0.25+i*0.094,0.26+i*0.094,0.155,'0xDEDEDE',5),msg='?????????')
                for file_item in os.listdir('figures/item_daily'):
                    if 'acc'+str(acc) in file_item:
                        item = cv2.imread('figures//item_daily//'+str(file_item))
                        item = cv2.cvtColor(item, cv2.COLOR_RGB2BGR)
                        img_pos = self.ImgExist((0,0,1,1,item, 0.1,1400,786),pos=1)
                        if img_pos[0]>0.95:
                            self.myclick( (img_pos[1],img_pos[2]), delay=1, color_info=(0.67,0.80,0.68,0.81,'0xD6DA28',5), mode=1,msg='????????????')
                            if self.PixelExist((0.78,0.65,0.79,0.66,'0x6B6152',0.5)):
                                self.myclick((0.785,0.65),delay=0.5)
                            self.myclick((0.678,0.805),delay=0.5)
                            while self.ImgExist((0,0,1,1,item, 0.95,1400,786)): # ??????????????????
                                pass
            self.home_screen()
            
            friends = self.lst_friends[acc-1]
            if len(friends)>0:
                self.myclick(key_friend, delay=delay, color_info=color_graycross, msg='????????????', mode=2)
                self.myclick((0.681, 0.346), delay=1, color_info=(0.246,0.917,0.246,0.917,'0xD6DA29',0), mode=1)
                self.myclick((0.246,0.917), delay=1, msg='????????????', color_info=(0.246,0.917,0.246,0.917,'0xDEDEDE',0), mode=1)
                self.myclick((0.149,0.869), delay=0.3, msg='????????????')
                self.myclick((0.164,0.8), delay=0.3, msg='?????????')

                self.myclick((0.492,0.162), delay=0.1, msg='????????????')
                self.myclick((0.492,0.162), delay=0.1)
                self.myclick((0.492,0.162), delay=0.1)
                self.myclick((0.492,0.162), delay=0.1)

                for friend in friends:
                    num_friend = friend-1
                    row_friend, col_friend = num_friend//5, num_friend%5
                    self.myclick( (0.681+col_friend*0.062, 0.257+row_friend*0.136), delay=0.2)
                self.myclick((0.944,0.939), delay=1, msg='????????????', color_info=(0.944,0.939,0.944,0.939,'0xD6DA29',0), mode=3)
                if self.PixelExist((0.573,0.598,0.573,0.598,'0xD6DA29',0)):
                    self.myclick((0.573,0.598), delay=1, msg='??????')
                else: 
                    print('??????????????????')
                self.home_screen()
            ## ????????????
            self.myclick((0.75,0.055), delay=1)
            for i in range(0,4):
                self.myclick((0.75,0.95), delay=0.3)
            self.myclick((0.5,0.16), delay=1)
            for i in range(0,4):
                self.myclick((0.75,0.95), delay=0.3)                
        self.checkusing = 1
        
    def pvp(self, delay=1):
        tz = pytz.timezone('Asia/Taipei')
        if datetime.now(tz).isoweekday()==7: # ??????????????????
            return        
        if self.d_pvp==clock2('day'): # ?????????????????????
            return
        if not self.enable_pvp: # ??????????????????
            return
        lower = self.hour_start_pvp*60 + self.min_start_pvp
        upper = self.hour_end_pvp*60 + self.min_end_pvp
        t_now = clock2()
        if t_now>upper:
            self.d_pvp=clock2('day')
            return
        elif t_now<lower:
            return
        if self.mode == 'economic':
            self.mode='basic'
            self.home_screen()
        print('pvp ?????????')
        start_fight = (0.855,0.945,0.860,0.950,'0xD6DA29',5)
        # PVP????????????????????????
        if self.mode!='pvp':
            self.myclick(key_list, delay=delay, color_info=color_graycross, msg='????????????', mode=2)
            self.myclick((0.891, 0.345), delay=delay, color_info=(0.03,0.95,0.03,0.95,'0x6B6152',0), msg='?????????', mode=1)
        
            if not self.PixelExist(start_fight):
                print('??????????????????')
                self.mode = 'basic'
                return
            if self.until_reward and self.PixelExist((0.796, 0.786, 0.796, 0.786, '0x7F3F00',0)) and self.PixelExist((0.978, 0.786, 0.978, 0.786, '0x5A5A5A',0)):
                print('????????????????????????')
                self.d_pvp = clock2('day')
                self.mode = 'basic'
                return            
        
        self.mode = 'pvp'
        self.home_screen(checkmode=True)
        self.eat_potion(check_sp=self.sp_pvp, check_ep=self.ep_pvp)
        
        self.myclick(key_list, delay=delay, color_info=color_graycross, msg='????????????', mode=2)
        self.myclick((0.891, 0.345), delay=delay, color_info=(0.03,0.95,0.03,0.95,'0x6B6152',0), msg='?????????', mode=1)
        
        
        if not self.PixelExist(start_fight):
            print('??????????????????')
            self.mode = 'basic'
            return
        if self.until_reward and self.PixelExist((0.796, 0.786, 0.796, 0.786, '0x7F3F00',0)) and self.PixelExist((0.978, 0.786, 0.978, 0.786, '0x5A5A5A',0)):
            print('????????????????????????')
            self.d_pvp = clock2('day')
            self.mode = 'basic'
            return            

        self.myclick((0.858, 0.949), delay=delay, color_info=color_graycross, msg='????????????', mode=4)
        self.myclick((0.63, 0.565), delay=delay)

        keep = True
        finish_lose = (0.532,0.622,0.532,0.622,'0x6B6152',3) # ??????????????????
        finish_win = (0.532,0.710,0.532,0.710,'0x6B6152',3)  # ??????????????????
        
        finish2 = (0.607,0.432,0.607,0.432,'0xFFFFFF',0) # ????????????????????????????????????
        while keep:
            print('??????????????????????????????')
            if self.PixelExist((0.625,0.675,0.630,0.68,'0xD6DA29',3)): # ????????????
                self.myclick( (0.627, 0.676), delay=delay, msg='??????')
            elif self.PixelExist((0.566, 0.547, 0.566, 0.547,'0xD6DA29',3), shot=0): # ?????????????????????
                self.myclick( (0.566, 0.547), delay=delay, msg='??????')
            elif (self.PixelExist(finish_lose, shot=0) or self.PixelExist(finish_win, shot=0)) and self.PixelExist(finish2, shot=0):
                least = 0.5
                t_start = time.time()
                while time.time()-t_start<least and (self.PixelExist(finish_lose, shot=0) or self.PixelExist(finish_win, shot=0)) and self.PixelExist(finish2): 
                    pass
                if time.time()-t_start>least: # least time of self.PixelExist(finish) 
                    self.myclick((0.537, 0.62), delay=delay, msg='????????????, ??????')
                    self.myclick((0.537, 0.71), delay=delay, msg='????????????, ??????')
                    keep=False
            elif self.enable_debuff and self.ImgExist((0.2, 0.2, 0.8, 0.8, knockout, 0.7, 1400, 786), shot=0) and time.time()-self.t_debuffskill>10:
                self.t_debuffskill = time.time()
                self.switch_page(self.page_debuffskill)
                for i in range(0,10):
                    self.myclick(self.key_debuffskill, delay=0.2, msg='????????????')
                self.switch_page(1)
            time.sleep(1)

            t_now = clock2()
            if t_now > upper:
                return
        time.sleep(3)
        while not self.checkhome_screen():
            print('loading')
            time.sleep(1)
        self.fight(1)
        
    ################
    ### checking ###
    ################
    def waitloading(self, timemax=30):
        if self.title!='Moonlight_Global':
            timemax = 120
        t_start=time.time()
        t_print=0
        while not self.checkloading(): # ????????????loading
            if time.time()-t_print>1:
                print('????????????loading...')
                t_print = time.time()
            if time.time()-t_start>timemax:
                raise ValueError('????????????-waitloding')
            time.sleep(0.1)

        time.sleep(3)        
        while self.checkloading(): # ????????????loading
            if time.time()-t_print>1:
                print('????????????loading...')
                t_print = time.time()
            if time.time()-t_start>timemax:
                raise ValueError('????????????-waitloding')
            time.sleep(0.1)
        time.sleep(2)
    def checkloading(self):
        try:
            return(self.ImgExist((0.470, 0.460, 0.530, 0.510, loading, 0.85, 1400, 786)))
        except:
            print('error-checkloading')
    def checkweight(self):
        return self.PixelExist( (892/960, 37/540, 892/960, 39/540, "0xECA647", 10)) # blue bar
    def checkbagfull(self):
        # print(self.ImgExist((0.4,0.28,0.595,0.34,bag_fullgray, 0.5, 1135, 637),value=1))
        self.screenshot()
        h, w, _ = self.img.shape
        x1, y1 , x2, y2 = int(0.400*w), int(0.280*h), int(0.595*w), int(0.340*h)        
        img_sub = self.img[y1:y2, x1:x2,]
        img_subgray = cv2.cvtColor(img_sub,cv2.COLOR_BGR2GRAY)
        return ImgSearch(bag_fullgray, img_subgray, threshold=0.4, x_scale = w/1135, y_scale=h/637)
    def checkdead(self, shot=1):
        if shot:
            self.screenshot()
        E1 = self.PixelExist((0.5, 0.600, 0.5, 0.600, '0xD4D725', 5), shot=0) # search middle blue
        E2 = self.PixelExist((0.5, 0.666, 0.5, 0.666, '0x6B6152', 5), shot=0) # search middle gray
        return (E1 and E2)
    def check_equip_and_statue(self, shot=1):
        if shot:
            self.screenshot()
        img_now=self.img
        v1=self.ImgExist((0.123, 0.877, 0.162, 0.953, change1, 0.1, 1400, 786), img=img_now, pos=1)[0]
        v2=self.ImgExist((0.123, 0.877, 0.162, 0.953, change2, 0.1, 1400, 786), img=img_now, pos=1)[0]
        v3=self.ImgExist((0.123, 0.877, 0.162, 0.953, change3, 0.1, 1400, 786), img=img_now, pos=1)[0]
        equip = np.argmax([v1, v2, v3])+1

        v1=self.ImgExist((0.168, 0.877, 0.207, 0.953, change1, 0.1, 1400, 786), img=img_now, pos=1)[0]
        v2=self.ImgExist((0.168, 0.877, 0.207, 0.953, change2, 0.1, 1400, 786), img=img_now, pos=1)[0]
        v3=self.ImgExist((0.168, 0.877, 0.207, 0.953, change3, 0.1, 1400, 786), img=img_now, pos=1)[0]
        statue = np.argmax([v1, v2, v3])+1
        return((equip, statue))
    def check_fight(self, shot=1):
        if shot:
            self.screenshot()
        img_now=self.img
        if not self.PixelExist(color_fight, img=img_now):
            return 0
        else:
            v1=self.ImgExist((0.263, 0.887, 0.3, 0.957, auto, 0.1, 1400, 786), img=img_now, pos=1)[0]
            v2=self.ImgExist((0.263, 0.887, 0.3, 0.957, semi, 0.1, 1400, 786), img=img_now, pos=1)[0]
            if v1>v2:
                return 1
            else:
                return 2
    def checkhome_screen(self, shot=1):
        if shot:
            self.screenshot()
        E1 = self.PixelExist(color_info=color_redblood, shot=0)
        E2 = self.PixelExist(color_info=color_graycross, shot=0)
        E3 = self.PixelExist(color_info=color_whitebell, shot=0)
        return( E1 and (not E2) and E3 )
    def check_map_position(self, shot=1):
        if shot:
            self.screenshot()
        while not self.PixelExist(color_graycross):
            self.myclick((900/960, 200/540), delay=0.5, msg='????????????')
        while True:            
            posi = self.ImgExist((0.584, 0.106, 0.999, 0.842, mapposition, 0.1, 1400, 786), pos=1)
            if self.PixelExist((posi[1], posi[2]-0.01, posi[1], posi[2]-0.01, '0xFFFFFF',0)):
                break
        return (posi[1], posi[2])
        
    def BossExist(self, img=None):
        if type(img)==type(None):
            self.screenshot()
            img = self.img
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = img_gray.shape
        E1 = E2 = (0,0,0)
        #for scale in np.linspace(0.5, 1.4, 20)[::-1]:
        for scale in np.linspace(0.7, 1.3, 8)[::-1]:
            E1_s = ImgSearch(icon_lwgray, img_gray, threshold=0.8, x_scale=w/1322*scale, y_scale=h/742*scale, pos=1)
            E2_s = ImgSearch(icon_rwgray, img_gray, threshold=0.8, x_scale=w/1322*scale, y_scale=h/742*scale, pos=1)
            if E1_s[0]>E1[0]:
                E1 = E1_s
            if E2_s[0]>E2[0]:
                E2 = E2_s
            if E1[0]>0.8 or E2[0]>0.8: # early stop
                print('scale = '+str(scale))
                break
        if E1[0]>0.8 and E2[0]>0.8:
            x, y = (E1[1]+E2[1])/2/w, (E1[2]+E2[2])/2/h
        elif E1[0]>0.8:
            x, y = E1[1]/w+0.1, E1[2]/h
        elif E2[0]>0.8:
            x, y = E2[1]/w-0.09, E2[2]/h
        else:
            self.boss_status = max(0, self.boss_status-1)
            print('???????????????: '+str(self.boss_status))
            return 0, 0

        # if boss exist
        self.boss_status = self.boss_status_max
        print('??????????????? ('+str(round(x,3))+','+ str(round(y+0.14,3))+')')
        return x, y+0.14   
        
        
    ###########################
    ### debugging and tools ###
    ###########################
    def is_WinActive(self):
        if self.title == 'Moonlight_Global':
            return(self.hwnd==win32gui.GetForegroundWindow())
        else:
            return(self.hwnd0==win32gui.GetForegroundWindow())    
    def resizeWindow(self):
        self.checkerror()
        
        if 'UnityWndClass' in win32gui.GetClassName(self.hwnd):
            w_target, h_target = 1400, 786
        elif 'LDPlayer' in win32gui.GetClassName(self.hwnd0):
            w_target, h_target = 1402, 824
        elif 'WindowOwnDCIcon' in win32gui.GetClassName(self.hwnd0):
            w_target, h_target = 1402, 822

        if character_id!='Moonlight_Global':    
            self.hwnd = self.hwnd0
            _, _, w, h = self.getWindowRect()
            if (w-2)/(h-36)>1.8:
                self.myclick((0.99,0.03), delay=0.2)
        x, y, w, h = self.getWindowRect()
        X, Y = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

        y0 = y
        if x>X:
            x0 = x-X
        else:
            x0 = x       
        x0 = min(X-w_target, x0)
        y0 = min(Y-(h_target+100), y0)        
        if x>X:
            x0 = x0+X        
        if w==w_target and x0+w_target<X and y0+(h_target+100)<Y:
            if character_id!='Moonlight_Global':    
                self.hwnd = self.hwnd1
            return        
        win32gui.MoveWindow(self.hwnd, x0-calibration[0], y0-calibration[1], w_target+calibration[0]-calibration[2], h_target+calibration[1]-calibration[3], True)
        if character_id!='Moonlight_Global':
            self.hwnd = self.hwnd1
        time.sleep(0.01)
    def getPosition(self):
        x0, y0 = win32gui.GetCursorPos()
        x1, y1, w, h = self.getWindowRect()
        if 0<x0-x1 and x0-x1<w and 0<y0-y1 and y0-y1<h:
            self.screenshot()
            rgb = self.img[y0-y1, x0-x1,]            
            return( round((x0-x1)/w,3), round((y0-y1)/h,3), rgb_to_hex(tuple(rgb)) )
        else:
            return( round((x0-x1)/w,3), round((y0-y1)/h,3) )
    def check_WindowRect(self, vertex = 1):
        rect = self.getWindowRect()
        if vertex:
            win32api.SetCursorPos((rect[0],rect[1]))
        else:
            win32api.SetCursorPos((rect[0]+rect[2],rect[1]+rect[3]))
    def gameloop(self):
        self.checkusing = -1
        self.myclick(key_info)
        self.checkusing = 1        
        while True:
            try:
                self.print_info()
                self.home_screen(delay=delay, checkmode=True)

                self.food()             # ????????????
                self.sell(delay=delay)              # ?????????
                self.decompose(delay=delay)         # ????????????
                self.storage(delay=delay)           # ????????????
                self.auction(delay=delay)           # ?????????
                self.teamup(delay=delay)
                self.daily_raid(delay=delay) # ????????????
                self.normal_raid(delay=delay) # ????????????
                self.guild_hunt(delay=delay) # ????????????
                self.pvp(delay=delay) # ?????????PVP

                if '??????' in MAP:
                    self.FightBoss(BOSS='??????', tele1=1, tele2=2)                
                t_print = t_start = time.time()                
                while time.time() - t_start<5:
                    if time.time()-t_print>1:
                        t_print = time.time()
                        self.print_info()

                    if self.ultimate_water:
                        if self.PixelExist((0.082, 0.015, 0.20, 0.041, '0x220084',5)):
                            E = self.PixelExist((0.082, 0.015, 0.20, 0.041, '0x220084',5), shot=0, pos=1)
                            if (E[0]-0.082)/(0.2-0.082)<0.95 and time.time()-self.t_drinkwater>2:
                                self.t_drinkwater = time.time()
                                self.myclick("{F1}", delay=0.05, msg='??????')
                    # ????????????
                    if self.enable_debuff and self.ImgExist((0.2, 0.2, 0.8, 0.8, knockout, 0.7, 1400, 786)) and time.time()-self.t_debuffskill>10:
                        self.t_debuffskill = time.time()
                        self.switch_page(self.page_debuffskill)
                        for i in range(0,10):
                            self.myclick(self.key_debuffskill, delay=0.2, msg='????????????')
                            
                    time.sleep(0.05)
                print(time.time()-self.t_eco, self.mode)
                time.sleep(1)
                if time.time()-self.t_eco>600 and self.mode=='economic':
                    self.mode = 'basic'
                elif self.mode =='basic':
                    self.mode = 'economic'
                    
            except Exception as e:
                print(e)
                time.sleep(1)
################################ use import next time
    def red_point_detecter(self):
        pts_posi = []
        pts_type = []
        val, _, y_lim = self.ImgExist((0.059, 0.087,0.261, 0.933,achieve_level,0.85,1400,786),pos=1) # ??????????????????
        if val<0.85:
            y_lim = 0.95
        y_upper = 0.087
        while self.PixelExist((0.074, y_upper, 0.076, y_lim-0.04, '0x0000FF',0), shot=0):    
            cx, cy = self.PixelExist((0.074, y_upper, 0.076, y_lim-0.04, '0x0000FF',0), shot=0, pos=1)
            pts_posi.append( (cx, cy) )
            if self.PixelExist((cx+0.01, cy, cx+0.01, cy, '0xEEEEEE',-3), shot=0): # ?????????
                pts_type.append(1)
            elif self.PixelExist((cx+0.01, cy, cx+0.01, cy, '0xCECECE',-3), shot=0): # ?????????
                pts_type.append(2)
            elif self.PixelExist((cx+0.01, cy, cx+0.01, cy, '0xDEDEDE',-3), shot=0): # ?????????
                pts_type.append(3)
            y_upper = cy + 0.04
        return (pts_posi, pts_type)
    def get_reward(self):
        while True:
            if self.PixelExist(color_redblood):
                self.myclick((0.79, 0.28), delay=0.1, color_info=(0.93,0.127,0.93,0.127,'0x6B6152',0),mode=1, msg='????????????') # ??????
            elif not self.PixelExist((0.93,0.127,0.93,0.127,'0x6B6152',0)):
                self.myclick((0.5,0.02),delay=delay)

            pts_posi, pts_type = self.red_point_detecter()
            if 3 in pts_type: # ??????????????????: ??????
                h, w, _ = self.img.shape
                if self.PixelExist((0.479, 0.845,0.479, 0.845, '0xD6DA29',5)): #??????
                    cx, cy = 0.479, 0.845
                elif self.PixelExist((0.897, 0.557,0.897, 0.557, '0xD6DA29',5)): #????????????
                    cx, cy = 0.897, 0.557
                else:
                    # ??????????????????????????????
                    if self.PixelExist((0.545, 0.522,0.545, 0.522,'0x39C4FF',0)) or self.PixelExist((0.554, 0.55,0.554, 0.55,'0xD5D827',0)):
                        c_x1, c_y1, c_x2, c_y2 = 0.262,0.522, 0.913, 0.854
                    # ??????
                    else:
                        c_x1, c_y1, c_x2, c_y2 = 0.262,0.181, 0.913, 0.854
                    img0 = self.img
                    while True:
                        img1 = self.screenshot()
                        diff_sub = img0[int(c_y1*h):(int(c_y2*h)+1), int(c_x1*w):(int(c_x2*w)+1),] - img1[int(c_y1*h):(int(c_y2*h)+1), int(c_x1*w):(int(c_x2*w)+1),]
                        a = np.sum(abs(diff_sub),axis=2)
                        if np.sum(a)>1000:
                            break
                    cy, cx = np.unravel_index(a.argmax(), a.shape)
                    cx, cy = (c_x1+cx/w, c_y1+cy/h)
                self.myclick((cx, cy), delay=0.5)
                self.myclick((0.5,0.02),delay=0.5)
            elif 2 in pts_type: # ???????????????????????????: ???????????????pts_type==2
                for i in range(0,len(pts_type)):
                    if pts_type[i]==2:
                        self.myclick(pts_posi[i],delay=delay)
                        break    
            elif 1 in pts_type: # ?????????????????????
                cx, cy = pts_posi[0]
                if self.PixelExist((cx, cy+0.078, cx+0.01, cy+0.079, '0xCECECE',-3),shot=0) or self.PixelExist((cx, cy+0.078, cx+0.01, cy+0.079, '0xDEDEDE',-3),shot=0):
                    print('?????????')
                    self.click(key=(0.2, 0.82), key2=(0.2, 0.15),press2=0.6)                                            
                else:
                    self.myclick((cx, cy),delay=1)
            else:
                self.home_screen()
                self.myclick((0.79, 0.28), delay=0.1, color_info=(0.93,0.127,0.93,0.127,'0x6B6152',0),mode=1, msg='????????????') # ??????
                val, _, y_lim = self.ImgExist((0.059, 0.087,0.261, 0.933,achieve_level,0.85,1400,786),pos=1) # ??????????????????
                pts_posi, pts_type = self.red_point_detecter()
                if len(pts_type)==0:
                    self.home_screen()
                    break   


# ??????: ??????(mx, my), ??????(f, fy), ??????(subregion), "???(region)" 
MAP = {
"??????": (628/960, 111/540,  31/960, 195/540),
"??????": (853/960, 122/540, 788/960, 155/540),
"???????????????": (691/960, 170/540, 769/960, 266/540),
"?????????": (731/960, 152/540, 890/960, 214/540),
"?????????": (787/960, 341/540, 609/960, 303/540),
"?????????": (820/960, 321/540, 847/960, 233/540),
"?????????": (776/960, 256/540, 890/960, 221/540),
"????????????": (620/960, 341/540, 659/960, 288/540),
"??????": (677/960, 228/540, 641/960, 292/540),
"?????????": (610/960, 360/540, 642/960, 260/540),
"?????????": (820/960, 118/540, 758/960, 217/540),
"?????????": (840/960, 120/540, 903/960, 144/540),
"?????????": (651/960, 407/540, 697/960, 150/540),
"??????": (771/960, 135/540, 783/960, 192/540),
"?????????": (771/960, 214/540, 910/960, 172/540, '???????????????', '???????????????'),
"?????????": (0.679, 0.752, 0.725, 0.259, "???????????????", "?????????"), 
"?????????": (0.704, 0.306, 0.727, 0.261, "???????????????", "?????????"), 
"???????????????": (0.656, 0.454, 0.676, 0.686, "??????????????????", "?????????"),
"?????????": (0.839, 0.545, 0.930, 0.339, "????????????", "?????????"),
"???????????????": (0.755, 0.46, 0.858, 0.285, "??????????????????", "?????????"),
"???????????????": (0.695, 0.364, 0.641, 0.217, "??????????????????", "?????????"),
"??????": (0.835, 0.731, 0.948, 0.648, "???????????????", "?????????"),
"?????????": (0.677, 0.341, 0.665, 0.346, "???????????????", "?????????")
}

SUBREGION = {
'???????????????': (0.77, 0.692),
'??????????????????': (0.79, 0.294),
'????????????': (0.696, 0.405),
'??????????????????': (0.82, 0.466),
'???????????????': (0.909, 0.423),
'??????????????????':(0.768, 0.601),
'???????????????':(0.89, 0.595),
'?????????????????????':(0.691, 0.756),
'???????????????':(0.778, 0.719),
'??????????????????':(0.784, 0.518)
}
REGION ={
"?????????????????????": (0.755, 0.246),
"?????????": (0.802, 0.209),
"???????????????": (0.789, 0.451),
"???????????????": (0.837, 0.482),
"????????????": (0.8, 0.584),
"?????????": (0.851, 0.572)    
}

color_graycross=(0.983, 0.05, 0.983, 0.05, '0x6B6152', 5)
color_graycross2=(0.6, 0.05, 0.6, 0.05, '0x6B6152', 5)
color_blueconfirm=(0.57, 0.595, 0.57, 0.595, '0xD6DA29', 10)
color_redblood=(0.082, 0.016, 0.102, 0.04,"0x6E44F3", 5)
color_whitebell=(0.695, 0.071, 0.696, 0.071, '0xFFFFFF', 0)
color_redpet=(0.007, 0.3, 0.007, 0.75, "0x6E44F3", 5)
color_waitloading=(478/960, 250/540, 478/960, 250/540, '0xFFFFFF', 0)
color_fight = (0.268, 0.912, 0.274, 0.933, '0xFFFFFF', 0)
color_pvpmode = (0.455, 0.28, 0.545, 0.385, '0x4856EE', 0)

        
os.system('chcp 936')
ep = cv2.imread('figures\\ep_1400x786.png')
sp = cv2.imread('figures\\sp_1400x786.png')                           
hpp = cv2.imread('figures\\hppotion_1400x786.png')
knockout = cv2.imread('figures\\knockout_1400x786.png')
back = cv2.imread('figures\\back_1400x786.png')
pageone = cv2.imread('figures\\pageone_1400x786.png')
change1 = cv2.imread('figures\\change1_1400x786.png')
change2 = cv2.imread('figures\\change2_1400x786.png')
change3 = cv2.imread('figures\\change3_1400x786.png')
auto = cv2.imread('figures\\auto_1400x786.png')
semi = cv2.imread('figures\\semi_1400x786.png')
pvpmode = cv2.imread('figures\\pvpmode_1400x786.png')
mapposition = cv2.imread('figures\\mapposition_1400x786.png')
passraid = cv2.imread('figures\\passraid_1400x786.png')
nextfloor1 = cv2.imread('figures\\nextfloor1_1400x786.png')
nextfloor2 = cv2.imread('figures\\nextfloor2_1400x786.png')
login_conflict = cv2.imread('figures\\login_conflict_1400x786.png')
loading = cv2.imread('figures\\loading_1400x786.png')
icon_burn = cv2.imread('figures\\icon_burn_1919x1015.jpg')
icon_poison = cv2.imread('figures\\icon_poison_1600x900.png')
icon_rw = cv2.imread('figures\\icon_rightwing_1322x742.png')
icon_lw = cv2.imread('figures\\icon_leftwing_1322x742.png')
icon_lwgray = cv2.cvtColor(icon_lw,cv2.COLOR_BGR2GRAY) # 1322x742
icon_rwgray = cv2.cvtColor(icon_rw,cv2.COLOR_BGR2GRAY) # 1322x742
food_effect = cv2.imread('figures\\food_effect_1473x827.png') # 1473x827
password_teamup2 = cv2.imread('figures\\password_teamup2_1400x786.png') # 0.95
bag_full = cv2.imread('figures\\bag_full_1135x637.png') # 1135x637
bag_fullgray = cv2.cvtColor(bag_full,cv2.COLOR_BGR2GRAY) # 1135x637
achieve_level = cv2.imread('figures\\achieve_level_1400x786.png')

## ??????????????????; ??????????????????????????????
key_burn =  0 # "{F5}" # ?????????????????????; ????????????????????????
key_poison = 0 # "{F4}" # ?????????????????????; ????????????????????????


########## ??????????????????
if character_id == 'Moonlight_Global':
    calibration = (8, 32, -9, -9) # ??????????????????
else:
    calibration = (0, 0, 0, 0) # ??????????????????
delay = 1 # ??????????????????
keywait = 0.3 # ?????????????????????????????????
checkusing = 1 # ?????????????????????
exe = 0 # 0: ??????????????????, -1: ???????????????, 1: ???????????????
