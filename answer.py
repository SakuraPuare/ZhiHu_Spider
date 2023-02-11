import httpx

from database import SQL, Answer, User, Question

answer = ['2569033692', '2570936374', '2570374800', '2569272197', '2567391241', '2570192173', '2571757659',
          '2569095822', '2569040273', '2568145752', '2569145098', '2569992345', '2570992636', '2585296739',
          '2568892041']

sql = SQL()

url = 'https://api.zhihu.com/answers/'

answer_list = []
user_list = []
question_list = []
for i in answer:
    url = url + i + '?include=created_time,updated_time,voteup_count,favlists_count,comment_count,content,is_labeled,author.badge_v2'
    resp = httpx.get(url=url)
    data = resp.json()
    answer_list.append(data)
    user_list.append(data.get('author'))
    question_list.append(data.get('question'))

# if answer_list:
#     sql.insert_into('answer', Answer, answer_list)
#     pass
# if user_list:
#     sql.insert_into('user', User, user_list)
#     pass
if question_list:
    sql.insert_into('question', Question, question_list)
    pass
