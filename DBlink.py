import mysql.connector, time
from SQLapi import getSQL
mydb = None
def initDB():
    global mydb
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="zhangzhe",
        password="zhangzhe197",
        database="ProjectM"
    )
#====================================
# 这个函数的作用是格式化数据库中的数据,以便于在其他地方使用。

# 函数接受两个参数:
# 1. row: 一行数据,可能是从数据库中查询出来的一行记录。
# 2. role: 一个字符串,用于指定格式化的方式。如果role为'under',则使用一种格式化方式;否则使用另一种格式化方式。
# 当role为'under'时,函数会按照以下格式输出:
# 1. 输出最低录取分数和最低录取排名,包括2023年和2022年的数据。
# 2. 如果有就业率和升学率数据,则输出;否则输出"no employment rate and enrollment rate"。
# 3. 如果有主修课程信息,则输出;否则输出"no major coures information"。
# 4. 输出描述信息。
# 当role不为'under'时,函数会将每个元素(可能是一个字段)用" +"和换行符连接起来,并返回这个字符串。
#====================================
def format_DB_data(row, role):
    if role == 'under':
        rankAndScore = f'''
{row[1]},2023 Minimum Admission Score is {row[2]}. 2023 Minimum Admission rank is {row[3]}.
2022 Minimum Admission Score is {row[4]}, 2022 Minimum Admission rank is {row[5]}.\n
  ''' 
        enrollment = (f"in 2021, employment rate is {row[7]}%, 升学率 is {row[8]}%\n" 
                  if row[7] is not None else 
                  "no employment rate and enrollment rate\n") 
        Major_course = f"Major course are {row[9]} \n" if row[9] is not None else "no major coures information\n"
        description = f'''
        description:
        {row[6]}'''
        return rankAndScore + enrollment + Major_course + description
    else: 
        res = ""
        for element in row:
            res += (element + " +\n")
        return res
#====================================
# 该函数用于执行数据库查询并格式化查询结果。
# 参数:
# order: 要执行的SQL查询语句
# role: 用于格式化查询结果的角色
# 返回值:
# 格式化后的前3条查询结果, 如果查询结果少于3条则返回全部结果。
# 同时会打印找到的记录数。
#====================================
def makeInquire(order, role):
    res = ""
    cnt = 0
    try:
        mycursor = mydb.cursor()
        mycursor.execute(order)
        results = mycursor.fetchall()
        for row in results[:3]:
            cnt += 1
            res += format_DB_data(row,role)
                    
        mycursor.close()
    except Exception as e:
        print("数据库查询错误:"+e)
        
    print(f"找到{cnt}条记录")
    return res

#====================================
# 解释内容
# 该函数用于从数据库中获取信息,根据输入的问题和角色来构建SQL查询语句,并返回补充提示内容。
# 函数逻辑:
# 1. 初始化 Supplementary_prompt_content 变量为空字符串
# 2. 调用 getSQL 函数,根据 question 和 role , 调用SQL大模型, 获取 SQL 查询语句 order
# 3. 判断 order 是否以 "SELECT" 开头,如果是,则调用 makeInquire 函数,将 order 和 role 作为参数,获取补充提示内容 Supplementary_prompt_content
# 4. 如果 order 不是以 "SELECT" 开头,则拒绝执行语句
# 6. 返回 Supplementary_prompt_content
#====================================

def getInfoFromDB(question,role):
    Supplementary_prompt_content = ""
    order = getSQL(question, role)
    point1 = time.time()
    if order.startswith("SELECT"):
        Supplementary_prompt_content = makeInquire(order, role)
    else : print("not formated")
    print(f"order = {order}, {Supplementary_prompt_content}")
    point2 = time.time()
    return Supplementary_prompt_content,(point1, point2)

#====================================
#
# 该函数用于从数据库中获取指定类型的文章列表,并根据需求对文章名称进行长度限制。
#
# 参数:
# article_type: 文章类型,用于筛选数据库中的文章
# maxNum: 最大返回的文章数量,默认为100
# length_limit: 是否对文章名称长度进行限制,默认为True
# 返回值:
# 如果length_limit为True,则返回一个列表,列表中每个元素为一个包含文章id、文章名称(长度小于25个字符)和发布日期的列表。
# 如果length_limit为False,则返回一个包含文章id、文章名称和发布日期的元组列表。
#
#====================================
def getArticleList(article_type,maxNum = 100, length_limit = True):
    mycursor = mydb.cursor()
    sql = "SELECT id, article_name,publish_date FROM articles WHERE article_type = %s ORDER BY publish_date DESC LIMIT %s"
    val = [article_type,maxNum]
    mycursor.execute(sql, val)
    results = mycursor.fetchall()
    mycursor.close()
    if length_limit:
        list_to_return = []
        for record in results:
            res = list(record)
            res[1] = res[1] if len(res[1]) < 25 else res[1][:25] + "..."
            list_to_return.append(res)
        return list_to_return
    else : return results
#====================================
# 该函数用于根据文章的 ID 或名称获取文章的内容。
#
# 参数:
# - id (可选): 文章的 ID
# - name (可选): 文章的名称
#
# 返回值:
# 返回文章的格式化 HTML 内容。如果同时传入 id 和 name,则优先使用 id 进行查询。
#
#====================================
def getArticleContent(id = None, name = None):
    mycursor = mydb.cursor()
    sql = None
    val = None
    if id is not None:
        sql = "SELECT formatted_html,article_name,publish_date FROM articles WHERE id = %s"
        val = [id]
    if name is not None:
        sql = "SELECT formatted_html FROM articles WHERE article_name = %s AND article_type = 'introduction'"
        val = [name]
    mycursor.execute(sql, val)
    res = mycursor.fetchall()
    mycursor.close()
    return res[0]

        