from Features.Features import Features
import time
features = Features()

if features.is_debugging() == True or features.is_virtualizing() == True:
    time.sleep(5)
    print('NGU')
else:
    print('OK')