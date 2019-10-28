# douban-to-imdb
导出豆瓣电影评分到IMDB，进而导入Trakt.

## 需求

* [pyenv](https://github.com/pyenv/pyenv)
* [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

## 初始化

    $ pyenv install 3.8.0
    $ pyenv virtualenv 3.8.0 douban-to-imdb-env
    $ pyenv activate douban-to-imdb-env
    $ pip install -r requirements.txt
    
###### *・如果不使用虚拟环境，请参照requirements.txt中的内容自行安装*
    
## 使用

#### 导出豆瓣电影评分到CSV文件

    $ python douban_to_csv.py [user_id]
    
*其中`[user_id]`为豆瓣的用户 ID，查找方法参见：[如何查找自己的豆瓣ID](https://github.com/pyenv/pyenv-virtualenv)*

#### 导入电影评分到IMDB

&ensp;&ensp;&ensp;由于导入IMDB需要登录，所以此过程需要打开浏览器，等待自行登录IMDB账号。登录成功后浏览器会自动查找电影并进行打分，这是正常的程序操作，并不是闹鬼，请勿惊慌。 👻👻👻

    $ python csv_to_imdb.py [unmark/-2/-1/0/1/2]
    
###### *・参数如果为 unmark时，则会清除CSV文件中电影对应的 IMDB中的评分*

###### *・参数如果为数字时，则打分时分调传入的数值，范围为 ±2分*

###### *・参数为空时，默认打分 -1分（由于豆瓣打分粒度太大，导致本人评分标准往往会比实际稍高 1分左右）*

###### *例：（无参数）*
  
###### *&ensp;&ensp;&ensp;豆瓣评五星：IMDB打 9分 （考虑到实际是能满分的电影比较少）*
  
###### *&ensp;&ensp;&ensp;豆瓣评一星：IMDB打 1分 （考虑到你既然都打一星了肯定是这电影烂到你恨不得给 0分）*
