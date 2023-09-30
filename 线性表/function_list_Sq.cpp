#include <iostream>
#include <process.h>
#define LIST_INIT_SIZE 100
#define LIST_INCREASEMENT 10
using namespace std;
typedef int ElemType;
typedef struct
{
    ElemType *elem;
    int length;
    int init_size;
    int increasement;

} List_Sq;

// ��ʼ˳���
void InitList_Sq(List_Sq &L)
{
    L.elem = new ElemType[LIST_INIT_SIZE];
    L.length = 0;
    L.init_size = LIST_INIT_SIZE;
    L.increasement = LIST_INCREASEMENT;
}

// ����˳���
void DestoryList_Sq(List_Sq &L)
{
    delete[] L.elem;
    L.init_size = 0;
    L.length = 0;
    cout << "˳��������٣�����" << endl;
}

// ���ÿձ�
void ClearList(List_Sq &L)
{
    if (L.length > 0)
    {
        L.length = 0;
        cout << "���Ա��Ѿ�����Ϊ�ձ�" << endl;
    }
    else
        cout << "���Ա����ڣ��޷�����Ϊ�ձ�" << endl;
}

// �ж��Ƿ�Ϊ�ձ�
bool ListEmpty(List_Sq &L)
{
    if (L.length == 0)
        return true;
    else if (L.length != 0)
        return false;
}

// �����Ա���
int ListLength(List_Sq &L)
{
    return L.length;
}

// ����˳���Ԫ��
ElemType GetElem(List_Sq &L, int i, ElemType e)
{
    if (i < 1 || i > L.length)
    {
        cout << "i��ֵ���Ϸ�,���������Ա�Χ" << endl;
        exit(1);
    }
    else
    {
        e = L.elem[i - 1];
        return e;
    }
}

// ����˳���Ԫ��λ��
int LocateElem(List_Sq &L, ElemType e)
{
    ElemType *p;
    p = L.elem;
    int i = 1;
    while (i <= L.length && *p++ != e)
        ++i;
    if (i > L.length)
        return 0;
    else
        return i;
}

// ����Ԫ��ǰ��
ElemType PriorElem(List_Sq &L, ElemType cur_e, ElemType &pre_e)
{
    int i = 0;
    while (L.elem[i] != cur_e)
    {
        i++;
    }
    if (i == 0)
    {
        cout << "Ԫ��cur_e�ǵ�һ��Ԫ��,û��ǰ��!" << endl;
        exit(1);
    }
    pre_e = L.elem[i - 1];
    return pre_e;
}

// ����Ԫ�غ��
ElemType NextElem(List_Sq &L, ElemType cur_e, ElemType &next_e)
{
    int i = 0;
    while (L.elem[i] != cur_e)
    {
        i++;
    }
    if (i == L.length - 1)
    {
        cout << "Ԫ��cur_e�����һ��Ԫ��,û�к��!" << endl;
        exit(1);
    }
    next_e = L.elem[i + 1];
    return next_e;
}

ElemType *a;
// ������������
void Increasement_Sq(List_Sq &L)
{

    a = new ElemType[L.init_size + L.increasement];
    for (int i = 0; i < L.length; i++)
        a[i] = L.elem[i];
    delete[] L.elem;
    L.elem = a;
    L.init_size += L.increasement;
}
// ����ָʾ����
void Errormessage(char *s)
{
    cout << s << endl;
    exit(1);
}
// ����˳���Ԫ��
void ListInsert(List_Sq &L, int i, ElemType e)
{
    if (i < 1 || i > L.length + 1)
        Errormessage("i��ֵ���Ϸ�");
    if (L.length >= L.init_size)
        Increasement_Sq(L);
    ElemType *q, *p;
    q = &(L.elem[i - 1]);
    for (p = &L.elem[L.length - 1]; p >= q; --p)
        *(p + 1) = *p;
    *q = e;
    L.length++;
}

// ɾ��˳���Ԫ��
void ListDelete(List_Sq &L, int i, ElemType &e)
{
    if (i < 1 || i > L.length)
        Errormessage("i��ֵ���Ϸ�");
    ElemType *q, *p;
    q = &(L.elem[i - 1]);
    e = *q;
    q = &(L.elem[L.length - 1]);
    for (p = &L.elem[i]; p <= q; ++p)
        *(p - 1) = *p;
    L.length--;
    cout << "ɾ����Ԫ��Ϊ:" << e << endl;
}

// �������Lÿ������Ԫ��
void ListTraverse(List_Sq &L)
{
    int i = 0;
    cout << "<";
    while (i < L.length - 1)
    {
        cout << L.elem[i] << " ";
        i++;
    }
    cout << L.elem[i] <<" >"<<endl;
}

void putp(List_Sq &L)
{
    char ch;
    int c = 1;
    cout << "��������Ҫ��˳���Ԫ��:" << endl;
    while ((ch = getchar()) != '\n')
    {
        if (ch == ' ')      continue;
        ListInsert(L, c, int(ch - '0'));
        c++;
    }
}
// A��B����
List_Sq Intersection_List_Sq(List_Sq &LA, List_Sq &LB)
{
    List_Sq LC;
    InitList_Sq(LC);
    for (int i = 0; i <= LA.length - 1; i++)
        for (int j = 0; j <= LB.length - 1; j++)
            if (LA.elem[i] == LB.elem[j])
                LC.elem[LC.length++] = LA.elem[i];
    cout << "A * B = ";
    return LC;
}
//A��B����
List_Sq addictation_List_Sq(List_Sq &LA, List_Sq &LB)
{
    List_Sq LD;
    InitList_Sq(LD);
    for (int i = 0; i <=LA.length-1; i++)
        LD.elem[LD.length++] = LA.elem[i];
    int k = LD.length - 1;
    for (int i = 0; i <= LB.length - 1; i++)
    {
        bool cmp = 0;
        for (int j = 0; j <= k; j++)
            if (LD.elem[j] == LB.elem[i])
                {
                cmp = 1;
                break;
                }
        if(!cmp)LD.elem[LD.length++] = LB.elem[i];
    }
    cout << "A U B = ";
    return LD;
}
// A��B� A-B
List_Sq subtraction_List_Sq(List_Sq &LA, List_Sq &LB)
{
    List_Sq LC;
    InitList_Sq(LC);
    for (int i = 0; i <= LA.length - 1; i++){
        bool cmp = 0;
        for (int j = 0; j <= LB.length - 1; j++)
            if(LA.elem[i]==LB.elem[j]){
                cmp = 1;
                break;
            }
        if(!cmp){
            LC.elem[LC.length++] = LA.elem[i];
        }
    }     

    return LC;
}
//��ʽ������
void putq(List_Sq &L)
{
    InitList_Sq(L);
    int n,m;
    cout << "num = ";
    cin >> n;
    cout << "elem = ";
    for (int i = 0; i < n; i++)
    {
       
        cin >> m;
        L.elem[L.length++] = m;
    }
}