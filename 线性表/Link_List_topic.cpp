#include <iostream>
#define N 10000
using namespace std;
typedef int ElemType;
typedef struct LNode
{
    ElemType data;
    struct LNode *next;

} LNode, *LinkList;
// 输入
void putp(LinkList &L)
{
    L = NULL;
    LNode *s;
    cout << "请输入需要的单链表元素的个数:" << endl;
    int n, f[N], m;
    cin >> n;
    cout << "请输入需要的单链表元素:" << endl;
    for (int i = 1; i <= n; i++)
        cin >> f[i];
    cout << "输入完毕！" << endl;
    for (int i = n; i >= 0; i--)
    {
        s = new LNode;
        if(n>=1)
        s->data = f[i];
        s->next = L;
        L = s;
    }
}
// 前插p结点
void ListInsert_L(LinkList &L, LNode *p, LNode *s)
{
    if (p == L->next)
    {
        s->next = p;
        L = s;
    }
    else
    {
        LNode *q;
        q = L->next;
        while (q->next && q->next != p)
            q = q->next;
        q->next = s;
        s->next = p;
    }
}
// 后插p结点
void ListInsert_N(LinkList &L, LNode *p, LNode *s)
{
    s->next = p->next;
    p->next = s;
}
// 求单链表长度
int List_Length(LinkList &L)
{
    LNode *p;
    int k = 0;
    p = L->next;
    while (p)
    {
        k++;
        p = p->next;
    }
    return k;
}
// 删除单链表结点
ElemType Delete_LinkList(LinkList &L, LNode *p, ElemType &e)
{
    if (p == L->next)
        L = p->next;
    else
    {
        LNode *q;
        q = L->next;
        while (q->next && q->next != p)
            q = q->next;
        q->next = p->next;
    }
    e = p->data;
    delete p;
    return e;
}
// 返回查找数据的指针
LNode *locate_LinkList(LinkList &L, ElemType &e)
{
    LNode *q;
    q = L->next;
    while (q && q->data != e)
        q = q->next;
    return q;
}
// 依次输出L每个数据元素
void Traverse_ListLink(LinkList &L)
{
    cout << "单链表每个数据元素:" << endl;
    LNode *p;
    p = L->next;
    while (p->next)
    {
        cout << p->data << " ";
        p = p->next;
    }
    cout << p->data << endl;
}

// 销毁顺序表
void Destory_ListLink(LinkList &L)
{
    LNode *p;
    while (L)
    {
        p = L;
        L = L->next;
        delete p;
    }

    cout << "顺序表已销毁！！！" << endl;
}

// 重置空表
void Clear_ListLink(LinkList &L)
{
    LNode *p;
    while (L->next)
    {
        p = L->next;
        L->next = p->next;
        delete p;
    }
}

// 判断是否为空表
bool Empty_ListLink(LinkList &L)
{
    if (L->next == NULL)
        return true;
    else
        return false;
}

// 返回顺序表元素位序
int Locate_ListLink(LinkList &L, ElemType e)
{
    LNode *p;
    p = L->next;
    int i = 1;
    while (p->data != e)
    {
        ++i;
        p = p->next;
    }

    if (i > List_Length(L))
        return 0;
    else
        return i;
}

// 返回元素前驱
LNode *Prior_ListLink(LinkList &L, LNode *p)
{
    int i = 0;
    LNode *q;
    q = L->next;
    while (q->next && q->next != p)
    {
        q = q->next;
        i++;
    }
    if (i == 0)
    {
        cout << "元素cur_e是第一个元素,没有前驱!" << endl;
        exit(1);
    }
    return q;
}

// 返回元素后驱
LNode *Last_ListLink(LinkList &L, LNode *p)
{
    int i = 0;
    LNode *q;
    q = L->next;
    while (q && q != p)
    {
        q = q->next;
        i++;
    }
    if (i >= List_Length(L))
    {
        cout << "元素cur_e是最后一个元素,没有后驱!" << endl;
        exit(1);
    }
    q = q->next;
    return q;
}
