#include <iostream>
#include "Link_List_topic.cpp"
using namespace std;
int main()
{
    LinkList la;
    int g; 
    putp(la);
    g = List_Length(la);
    cout << "la��˳�����:" << g << endl;
    Traverse_ListLink(la);
    system("pause");
    return 0;
}