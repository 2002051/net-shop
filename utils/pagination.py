# ######################yx自定义的分页组件#######################
"""
以后如果想要使用该封装组件，需要做如如下几件事，根据自己的情况
在视图函数里面
def pretty_list(request):
    # 1.根据自己的情况去筛选数据。
    queryset = models.PrettyNum.objects.all()

    # 2.实例化分页对象
    page_object = Pagination(request,queryset)

    # 3.

    context = {
         "search_data": search_data,  # 页码跳转框。
        "queryset": page_pbject.page_queryset,  # 分完页的数据
         'page_string': page_pbject.html()}  # 生成的页码的html代码
    }

在html代码里面

# 获取数据，拿到queryset 然后for循环
                    {% for x in queryset %}

                        <tr>
                            <td>{{ x.id }}</td>
                            <td>{{ x.mobile }}</td>
                            <td>{{ x.price }}</td>
                            {#                        <td>{{ x.level }}</td>#}
                            {#                        <td>{{ x.status }}</td>               这两个的结果直接展示存放的短整型数据，要想的到其映射的中文数据需要用get_字段名_display    #}
                            <td>{{ x.get_level_display }}</td>
                            <td>{{ x.get_status_display }}</td>
                            <td>
                                <a href="/mobile/{{ x.id }}/edit/" class="btn btn-primary">编辑</a> {# href一定要/开头#}
                                <a href="/mobile/delete/?nid={{ x.id }}" class="btn btn-danger">删除</a>
                                {# 吧id通过get请求传递给视图函数 #}
                            </td>

                        </tr>

                    {% endfor %}

# 获取页码
    <ul class = "pagination">
        {{page_string}}
     </ul>

"""

from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, request, queryset, page_size=10,
                 page_param="page", plus=5):  # 获取request对象以及,传入的page_param,默认值是"page" 然后通过request.GET.get来获取当前页。

        """

        :param request:  请求的对象
        :param queryset:  符合条件的数据（根据这个数据给他进行分页处理）
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中获取分页的参数
        :param plus: 显示当前页的 前后几页。
        """

        import copy
        query_dict = copy.deepcopy(request.GET)  # 拷贝一份,request.GET是不能直接修改的，因为后续还要不停的使用到这个方法。
        query_dict._mutable = True  # 把它改成可以修改的类型。
        self.query_dict = query_dict

        page = request.GET.get(page_param,
                               "1")  # page_param的默认值是page, 获取到当前页，并且用变量page来接收，而page_param所对应的其实就是get请求的时候传递数据所用的名字。
        #   如果没有写page_param的值就默认是1 但是如果是一个负数或者是中文等其它字符还需判断一下。

        if page.isdecimal():  # 判断page是否是十进制数。 注意此方法不能用于int型数据的判断只能用于str 所以默认值的1 应该改为"1"
            page = int(page)  # 那么就转成int类型
        else:  # 如果拿到的不是正常的页数量
            page = 1
        self.page = page  # 获取到当前页，用成员变量page来接收他
        self.page_size = page_size
        # print(page,type(page))

        # 根据当前页计算出起始值和结束值
        self.start = (page - 1) * page_size  # [0:10] start代替0的位置，end代替10的位置。
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]  # 接收到queryset即所有的数据然后根据计算，获取到当前页需要表示的部分数据

        total_count = queryset.count()  # 总共有多少条数据
        # 总页码
        total_page_count, div = divmod(total_count, page_size)  # 用两个变量来接收结果就可以了。
        if div:  # div表示的就是余数，如果没有整除，那么余数的值就不为0，而众所周知，只有当数的值为零 其布尔值才为false，其它情况都为True
            total_page_count += 1  # 如果没有整除，那么实际页数应该要比商多1，比如一页5个数据 11 个数据就需要用2+1页来表示。
        # 然后再封装一下总页码的数量。再外面就可以通过对象.total_page_count 来使用这个值了。
        self.total_page_count = total_page_count
        self.plus = plus
        self.page_param = page_param

    def html(self):
        #  把所有的生成分页功能的页码的代码全部放在这里

        if self.total_page_count <= 2 * self.plus + 1:  # 页数1-11页的话，无论第几页就都全部显示这些页
            # 数据库数据比较少，就
            start_page = 1
            end_page = self.total_page_count + 1  # 如果只小于十一页，那么只显示1-当前页+1
        # 计算出当前页的前五页和后五页。
        else:  # 如果总页数大于11页面
            if self.page <= self.plus:  # 当前页小于等于5
                start_page = 1
                end_page = 2 * self.plus + 1

                # 当前页大于5，要判断极值了
            elif self.page >= self.total_page_count - 5:  # 当前页比最大页面小5，那么就不能显示前五页后五页了
                start_page = self.total_page_count - 2 * self.plus
                end_page = self.total_page_count + 1  # 那么末尾页就是极值，但是记得加1因为range函数是前闭后开的哦
            else:
                start_page = self.page - self.plus  # 其它情况一切正常，显示当前页的前五页和后五页。
                end_page = self.page + self.plus + 1

        # 自动生成这种页码
        # <li><a href="/mobile/list/?page=2">2</a></li>
        # <li><a href="/mobile/list/?page=3">3</a></li>
        # <li><a href="?page=4">4</a></li>

        page_str_list = []

        self.query_dict.setlist(self.page_param, [1])

        last = f'<li><a href="?{self.query_dict.urlencode()}">首页</a></li>'
        page_str_list.append(last)
        # 上一页
        if self.page == 1:  # 第一页没有上一页
            self.query_dict.setlist(self.page_param, [1])
            prev = f'<li><a href="?{self.query_dict.urlencode()}">上一页</a></li>'
            page_str_list.append(prev)  # 把上一页标签压入列表的第一个
        else:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = f'<li><a href="?{self.query_dict.urlencode()}">上一页</a></li>'
            page_str_list.append(prev)  # 把上一页标签压入列表的第一个

        for i in range(start_page, end_page):
            if i == self.page:  # 如果i等于当前页，就给它的按钮标签加一个样式
                self.query_dict.setlist(self.page_param, [i])
                ele = f'<li class="active"><a href="?{self.query_dict.urlencode()}">{i}</a></li>'  # 每次循环生成一个li
            else:
                self.query_dict.setlist(self.page_param, [i])
                ele = f'<li><a href="?{self.query_dict.urlencode()}">{i}</a></li>'  # 每次循环生成一个li
            # 然后把它添加到列表里面。
            page_str_list.append(ele)

        # 下一页
        if self.page == self.total_page_count:  # 如果是最后一页
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            beh = f'<li><a href="?{self.query_dict.urlencode()}">下一页</a></li>'
        else:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            beh = f'<li><a href="?{self.query_dict.urlencode()}">下一页</a></li>'
        page_str_list.append(beh)
        # 列表是有顺序的，所以第一页标签放在第一个，下一页标签放在最后一页面。
        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        last = f'<li><a href="?{self.query_dict.urlencode()}">尾页</a></li>'
        page_str_list.append(last)

        # else:
        #     page_str_list = []
        #     for i in range(start_page, end_page):
        #         if i == page:  #如果i等于当前页，就给它的按钮标签加一个样式
        #             ele = f'<li class="active"><a href="?page={i}">{i}</a></li>'  # 每次循环生成一个li
        #         else:
        #             ele = f'<li><a href="?page={i}">{i}</a></li>'  # 每次循环生成一个li
        #         # 然后把它添加到列表里面。
        #         page_str_list.append(ele)

        search_string = """ 
                                <li>
                                <form style="float: left;margin-left:-1px" method="get" action = "?">
        
                                        <input name="page" style="position:relative;float:left;display:inline-block;width:80px;border-radius:0;"
                                              type="text"  class="form-control" placeholder="页码"  >
                                        <button style="border-radius:0" class="btn btn-default" type="submit" >跳转</button>
                                        
        
                                </form>
                                </li>
                                """

        page_str_list.append(search_string)

        page_string = mark_safe("".join(
            page_str_list))  # 用mark_safe来包裹这个标签，就可以把它当成标签来对待，否则就是长得和HTML代码一样的字符串, 需要进行导入：from django.utils.safestring import mark_safe
        # 这里的意思就是把join里面的每一个元素依次取到，中间都拼接上''字符串，这里的结果是一个字符串，html只会把他当成字符串，如果想要html把它被当成字符串的形式来对待，那么就应该
        return page_string  # 返回 page_string 然后再外面就可以直接使用对象.html来得到这串分页代码。
