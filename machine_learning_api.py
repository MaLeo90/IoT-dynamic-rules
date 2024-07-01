from androguard.core.bytecodes.apk import APK
import requests
import json
from keys import ml_url

class Parser:
	def __init__(self):
		self.current_line = []
		self.permissions_danger = {'signature|development|appop': '3', '': '0', 'signature|installer': '2', 'signature|privileged': '2', 'system|signature': '2', 'signature|privileged|installer': '3', 'normal': '1', 'signature|preinstalled|appop|pre23': '1', 'signature|preinstalled|appop|pre23|development': '2', 'signature|privileged|development|appop': '3', 'dangerous': '4', 'signature|privileged|development': '3', 'signatureOrSystem': '3', 'signature|system|development': '3', 'signature|system': '2', 'signature': '2'}
		self.all_permissions = ["ACCEPT_HANDOVER","ACCESS_CHECKIN_PROPERTIES","ACCESS_COARSE_LOCATION","ACCESS_FINE_LOCATION","ACCESS_LOCATION_EXTRA_COMMANDS","ACCESS_NETWORK_STATE","ACCESS_NOTIFICATION_POLICY","ACCESS_WIFI_STATE","ACCOUNT_MANAGER","ADD_VOICEMAIL","ANSWER_PHONE_CALLS","BATTERY_STATS","BIND_ACCESSIBILITY_SERVICE","BIND_APPWIDGET","BIND_AUTOFILL_SERVICE","BIND_CARRIER_MESSAGING_SERVICE","BIND_CARRIER_SERVICES","BIND_CHOOSER_TARGET_SERVICE","BIND_CONDITION_PROVIDER_SERVICE","BIND_DEVICE_ADMIN","BIND_DREAM_SERVICE","BIND_INCALL_SERVICE","BIND_INPUT_METHOD","BIND_MIDI_DEVICE_SERVICE","BIND_NFC_SERVICE","BIND_NOTIFICATION_LISTENER_SERVICE","BIND_PRINT_SERVICE","BIND_QUICK_SETTINGS_TILE","BIND_REMOTEVIEWS","BIND_SCREENING_SERVICE","BIND_TELECOM_CONNECTION_SERVICE","BIND_TEXT_SERVICE","BIND_TV_INPUT","BIND_VISUAL_VOICEMAIL_SERVICE","BIND_VOICE_INTERACTION","BIND_VPN_SERVICE","BIND_VR_LISTENER_SERVICE","BIND_WALLPAPER","BLUETOOTH","BLUETOOTH_ADMIN","BLUETOOTH_PRIVILEGED","BODY_SENSORS","BROADCAST_PACKAGE_REMOVED","BROADCAST_SMS","BROADCAST_STICKY","BROADCAST_WAP_PUSH","CALL_PHONE","CALL_PRIVILEGED","CAMERA","CAPTURE_AUDIO_OUTPUT","CAPTURE_SECURE_VIDEO_OUTPUT","CAPTURE_VIDEO_OUTPUT","CHANGE_COMPONENT_ENABLED_STATE","CHANGE_CONFIGURATION","CHANGE_NETWORK_STATE","CHANGE_WIFI_MULTICAST_STATE","CHANGE_WIFI_STATE","CLEAR_APP_CACHE","CONTROL_LOCATION_UPDATES","DELETE_CACHE_FILES","DELETE_PACKAGES","DIAGNOSTIC","DISABLE_KEYGUARD","DUMP","EXPAND_STATUS_BAR","FACTORY_TEST","FOREGROUND_SERVICE","GET_ACCOUNTS","GET_ACCOUNTS_PRIVILEGED","GET_PACKAGE_SIZE","GET_TASKS","GLOBAL_SEARCH","INSTALL_LOCATION_PROVIDER","INSTALL_PACKAGES","INSTALL_SHORTCUT","INSTANT_APP_FOREGROUND_SERVICE","INTERNET","KILL_BACKGROUND_PROCESSES","LOCATION_HARDWARE","MANAGE_DOCUMENTS","MANAGE_OWN_CALLS","MASTER_CLEAR","MEDIA_CONTENT_CONTROL","MODIFY_AUDIO_SETTINGS","MODIFY_PHONE_STATE","MOUNT_FORMAT_FILESYSTEMS","MOUNT_UNMOUNT_FILESYSTEMS","NFC","NFC_TRANSACTION_EVENT","PACKAGE_USAGE_STATS","PERSISTENT_ACTIVITY","PROCESS_OUTGOING_CALLS","READ_CALENDAR","READ_CALL_LOG","READ_CONTACTS","READ_EXTERNAL_STORAGE","READ_FRAME_BUFFER","READ_INPUT_STATE","READ_LOGS","READ_PHONE_NUMBERS","READ_PHONE_STATE","READ_SMS","READ_SYNC_SETTINGS","READ_SYNC_STATS","READ_VOICEMAIL","REBOOT","RECEIVE_BOOT_COMPLETED","RECEIVE_MMS","RECEIVE_SMS","RECEIVE_WAP_PUSH","RECORD_AUDIO","REORDER_TASKS","REQUEST_COMPANION_RUN_IN_BACKGROUND","REQUEST_COMPANION_USE_DATA_IN_BACKGROUND","REQUEST_DELETE_PACKAGES","REQUEST_IGNORE_BATTERY_OPTIMIZATIONS","REQUEST_INSTALL_PACKAGES","RESTART_PACKAGES","SEND_RESPOND_VIA_MESSAGE","SEND_SMS","SET_ALARM","SET_ALWAYS_FINISH","SET_ANIMATION_SCALE","SET_DEBUG_APP","SET_PREFERRED_APPLICATIONS","SET_PROCESS_LIMIT","SET_TIME","SET_TIME_ZONE","SET_WALLPAPER","SET_WALLPAPER_HINTS","SIGNAL_PERSISTENT_PROCESSES","STATUS_BAR","SYSTEM_ALERT_WINDOW","TRANSMIT_IR","UNINSTALL_SHORTCUT","UPDATE_DEVICE_STATS","USE_BIOMETRIC","USE_FINGERPRINT","USE_SIP","VIBRATE","WAKE_LOCK","WRITE_APN_SETTINGS","WRITE_CALENDAR","WRITE_CALL_LOG","WRITE_CONTACTS","WRITE_EXTERNAL_STORAGE","WRITE_GSERVICES","WRITE_SECURE_SETTINGS","WRITE_SETTINGS","WRITE_SYNC_SETTINGS","WRITE_VOICEMAIL","USES_SELF_DEFINED_PERMISSION"]
	def get_permissions(self,file_path):
		try:
			return APK(file_path).get_permissions()
		except:
			return([])
	def get_danger_level(self, file_path, permission):
		return self.permissions_danger[APK(file_path).get_details_permissions()[permission][0]]
	def parse(self, file_path):
		#self.apk_permissions = ["0" for x in range(len(permissions)+1)]
		loaded_permissions = self.get_permissions(file_path)
		self.current_line = ["0" for n in range(len(self.all_permissions)+1)]
		for i in loaded_permissions:
			#if("TOKEN" not in i):
			tmp = i.split(".")
			#print(tmp[len(tmp)-1] in self.all_permissions)
			if(not tmp[len(tmp)-1] in self.all_permissions):
				self.current_line[len(self.all_permissions)-1] = "1"
			else:
				self.current_line[self.all_permissions.index(tmp[len(tmp)-1])] = self.get_danger_level(file_path, i)
		#self.apk_permissions[len(self.apk_permissions)] = "?"
		self.current_line[len(self.all_permissions)] = "?"
		return ",".join(self.current_line)
	def send(self, file_path):
		#data = "{\"head\": \""+ HEAD+"\",\"data\": \""+self.parse(file_path)+"\"}"
		#headers = {'Content-Type': 'application/json'}
		data = self.parse(file_path)
		#print(ml_url+"/"+data)
		response = requests.get(ml_url+"/"+data)
		ans = response.text.split(",")
		return(ans[len(ans)-1])


