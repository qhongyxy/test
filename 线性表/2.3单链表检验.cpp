#include <iostream>
#include "Link_List.cpp"
using namespace std;
int main()
{
    LinkList la, lb, lc,ld;
    int g;
    putp(la);
    putp(lb);
    g = List_Length(la);
    cout << "la的顺序表长度:" << g << endl;
    Traverse_ListLink(la);
    lc=subtraction_LinkList(la, lb);
    Traverse_ListLink(lc);
    ld = and_LinkList(la, lb);
    Traverse_ListLink(ld);
    system("pause");
    return 0;
}