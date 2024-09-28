o
    ^�f�!  �                
   @   s  d dl Z d dlZd dlZd dlZd dlZd dlZd dlZd dlZd dlZd dl	Z	d dl
Z
d dlZd dlmZ d dlZdd� Zdd� Zdd� Zd	d
� Zdd� ZG dd� d�Zedkr�e� Zze��  W dS  ey� Z zeee�� e�d� W Y dZ[dS dZ[ww dS )�    N)�datetimec                 C   s@   d|  t ddd|  � d d||   d }t�|�t|� S )N�
   r   i�  i�  �   )�max�mathZfloor�value)�i�s�a�o�d�g�st� r   �bybit.py�calc   s   .r   c                 C   s    t �| �� |�� tj�}|�� S �N)�hmac�new�encode�hashlib�sha256Z	hexdigest)�key�messageZhmac_objr   r   r   �generate_hash
   s   r   c                 C   s   t j�| �S r   )�urllib�parse�unquote)Zencoded_urlr   r   r   �
url_decode   s   r   c                 C   s   t dd� | D ��d S )Nc                 s   s   � | ]}t |�V  qd S r   )�ord)�.0�charr   r   r   �	<genexpr>   s   � zvalue.<locals>.<genexpr>g     j�@)�sum)Z	input_strr   r   r   r      s   r   c                   C   sX   t t�d�� t t�d�� t t�d�� t t�d�� t t�d�� t �  t d� d S )Nur   ██     ██ ██ ███    ██ ███████ ███    ██ ██ ██████  uh   ██     ██ ██ ████   ██ ██      ████   ██ ██ ██   ██ ux   ██  █  ██ ██ ██ ██  ██ ███████ ██ ██  ██ ██ ██████  uj   ██ ███ ██ ██ ██  ██ ██      ██ ██  ██ ██ ██ ██      ur    ███ ███  ██ ██   ████ ███████ ██   ████ ██ ██      z/Join our Telegram channel: https://t.me/winsnip)�print�crayonsZbluer   r   r   r   �print_banner   s   r&   c                   @   sD   e Zd Zdd� Zdd� Zdd� Zdd� Zd	d
� Zdd� Zdd� Z	dS )�ByBitc                 C   s<   t �� | _ddddddd ddd	d
dddd�| _ddi| _d S )Nz!application/json, text/plain, */*zgzip, deflate, brz8en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,vi-VN;q=0.6,vi;q=0.5zapplication/jsonzhttps://bybitcoinsweeper.comzhttps://bybitcoinsweeper.com/zA"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"z?1z	"Android"�emptyZcorsz	same-siteztMozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.146 Mobile Safari/537.36)ZAcceptzAccept-EncodingzAccept-LanguagezContent-TypeZOriginZReferer�tl-init-dataz	Sec-Ch-UazSec-Ch-Ua-MobilezSec-Ch-Ua-PlatformzSec-Fetch-DestzSec-Fetch-ModezSec-Fetch-Sitez
User-Agent�scorer   )�requests�session�headers�info)�selfr   r   r   �__init__   s"   
�zByBit.__init__c                 C   sT   t jt jt jt jd�}t�� �d�}tt �	|�� d|�
|t j�|�� d|� �� d S )N)�INFO�ERROR�SUCCESS�WARNINGz%Y-%m-%d %H:%M:%S� | )r%   ZcyanZredZgreenZyellowr   Znow�strftimer$   Zwhite�get)r/   r   �levelZlevels�current_timer   r   r   �log3   s   �0z	ByBit.logc                 C   sj   t |dd�D ]!}t�dt�� �}tj�d|� d|� d�� tj��  t�d� qtj�d� tj��  d S )	Nr   �����z%H:%M:%Sz[z] [*] Waiting z seconds to continue...r   �)	�range�timer6   �	localtime�sys�stdout�write�flush�sleep)r/   Zsecondsr   �	timestampr   r   r   �wait=   s   
z
ByBit.waitc              
   C   s�   z8d|i| _ | jjdd|i| j d�}|jdkr3|�� }d|d � �| j d< d	|d |d
 |d d�W S ddd�W S  tjyR } zdt|�d�W  Y d }~S d }~ww )Nr)   z/https://api.bybitcoinsweeper.com/api/auth/loginZinitData��jsonr-   ��   zBearer �accessTokenZAuthorizationT�refreshToken�id)�successrJ   rK   ZuserIdFzUnexpected status code�rM   �error)r-   r,   �post�status_coderH   r+   �RequestException�str)r/   �	init_dataZresponse�datarO   r   r   r   �loginF   s    

���zByBit.loginc              
   C   sR   z| j jd| jd��� }|W S  tjy( } zdt|�d�W  Y d }~S d }~ww )Nz-https://api.bybitcoinsweeper.com/api/users/me)r-   FrN   )r,   r7   r-   rH   r+   rR   rS   )r/   �userrO   r   r   r   �userinfoX   s   ��zByBit.userinfoc              	   C   s  t d�D �]}z�d}d}t�||�}| jjdi | jd��� }d|v r3d|d v r3| �dd	� t�	d
� |d }|d }|d }| �
� }	| �d|	d |	d  � �d� t�|d�}
|
jtjd�}
t|
�� d �}| �d|d � d|� d�d� | �|� |	d � d�}|� d|� d|� �}|� d|� �}td|ddd|�}|d  |d! |d" ||t||�t|�d#�}| jjd$|| jd�}t|j� |jd%kr�| jd  |7  < | �d&d� n|jd'kr�| �d(d	� W  d)S | �d*|j� �d	� | �d+� W q tj�y
   | �d,d-� | �d.� Y qw dS )/N�   �2   �Z   z0https://api.bybitcoinsweeper.com/api/games/startrG   r   ZexpiredzQuery Expired Sirr2   r   rL   ZrewardsZ	createdAtzTotal Score: r*   ZscoreFromReferralsr3   z%Y-%m-%dT%H:%M:%S.%fZ)Ztzinfoi�  zStarting game r   z/3. Play time: z secondsr1   zv$2f1�-�-   �6   �	   T�bagCoins�bits�gifts)r`   ra   rb   ZgameIdZgameTime�hr*   z.https://api.bybitcoinsweeper.com/api/games/winrI   zGame Played Successfullyi�  z(Token expired, need to self.log in againFzAn Error Occurred With Code �   zToo Many Requests, Please Waitr4   �<   )r=   �randomZrandintr,   rP   r-   rH   r:   r@   �exitrX   r   �strptime�replace�pytzZUTC�intrE   rF   r   r   �floatr$   �textrQ   r.   r+   rR   )r/   r   Zmin_game_timeZmax_game_timeZ	game_timeZplaygameZgameidZ
rewarddataZ
started_atZuserdataZunix_time_startedZ	starttime�first�lastr*   Z	game_data�resr   r   r   r*   `   s^   

�	


�zByBit.scorec                 C   s�  t �t jdkr	dnd� t�  t j�t j�t�d�}t|ddd��}dd	� |D �}W d   � n1 s3w   Y  	 dd	� td�D �}t	|�D ]�\}}|rV||d t
|�  nd }|rd| jj�||d�� t|�}t|�}	t�|	�d�d �d�d �}
| �d|d � d|
d � d�d� | �d|
d � d�d� | �|�}|d r�| �dd� | �� }|s�| �dd� n| �d|d  � �d!� |t
|�d k r�| �d"� qF| �d"� q9)#N�nt�cls�clearzdata.txt�r�utf8)�encodingc                 S   �   g | ]
}|� � r|� � �qS r   ��strip�r    �liner   r   r   �
<listcomp>�   �    zByBit.main.<locals>.<listcomp>Tc                 S   rw   r   rx   rz   r   r   r   r|   �   r}   z	proxy.txtr   )�http�httpszuser=�&r   z========== Account r5   Z
first_namez ==========r1   zself.logging into account rL   z...rM   zlogin successful!r3   z5Need to self.log in again, moving to the next accountr4   zlogin failed! rO   r2   rY   )�os�system�namer&   �path�join�dirname�__file__�open�	enumerate�lenr,   �proxies�updater   rH   �loads�splitr:   rV   r*   rF   )r/   Z	data_file�frU   r�   r   rT   �proxy�decodedZfinaldatZ	user_dataZlogin_resultZgame_resultr   r   r   �main�   s<   �"
�
�
�z
ByBit.mainN)
�__name__�
__module__�__qualname__r0   r:   rF   rV   rX   r*   r�   r   r   r   r   r'      s    
	2r'   �__main__r   )r�   rH   r>   r+   r%   r@   �rer   r   rf   rj   r   r   �urllib.parser   r   r   r   r   r&   r'   r�   Zclientr�   �	Exception�errr$   rS   rg   r   r   r   r   �<module>   s(   ` 
 ���