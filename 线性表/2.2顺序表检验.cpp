#include <iostream>
#include "function_list_Sq.cpp"
using namespace std;
int main()
{
    List_Sq la,lb,lc;
   //  int g,l,m; 
    InitList_Sq(la);
    InitList_Sq(lb);
    InitList_Sq(lc);
   
    putp(la);
    putp(lb);
    //查询元素
      //  ElemType d,e,f;
    // cout << "请输入需要查询的元素:" << endl;
    // cin >> d;
    
   //输出顺序表长度
    // g = LocateElem(la, d);
    // cout << "la的顺序表长度:" << la.length << endl;

    // cout << "需要查找的元素的位序:" << g << endl;

    // cout << "请输入需要删除的元素的位序:" << endl;
    // cin >> l;
    // ListDelete(la,l,e);
    // ListTraverse(la);
    // cout << "la的顺序表长度:" << la.length << endl;

    // cout << "请输入需要插入的元素:" << endl;
    // cin >> f;
    // cout << "请输入需要插入的哪个位序元素之前:" << endl;
    // cin >> m;
   //  ListInsert(la, m, f);
   //  ListTraverse(la);
       lc=Intersection_List_Sq(la, lb);
       ListTraverse(lc);
    
       List_Sq ld;
       InitList_Sq(ld);
          ld = addictation_List_Sq(la, lb);
          ListTraverse(ld);
        List_Sq le;
       InitList_Sq(le);
          le = subtraction_List_Sq(la, lb);
          ListTraverse(le);
          List_Sq lf;
       InitList_Sq(lf);
          lf = subtraction_List_Sq(lb, la);
          ListTraverse(lf);
       system("pause");
       return 0;
}