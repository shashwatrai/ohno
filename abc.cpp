#include<bits/stdc++.h>
using namespace std;
int main()
{
	int t,n,m,i,j,ans,c,l,flag;

		cin>>n>>m;
		vector<pair<int,int> > a,b;
		for(i=0;i<n;i++)
		{
			cin>>l;
			a.push_back(make_pair(l,i));
		}
		for(j=0;j<m;j++)
		{
			cin>>l;
			b.push_back(make_pair(l,j));
		}
		sort(a.begin(),a.end());
		sort(b.begin(),b.end());
			for(i=0;i<m;i++)
				cout<<a[0].second<<" "<<b[i].second<<endl;
			for(i=1;i<n;i++)
				cout<<a[i].second<<" "<<b[m-1].second<<endl;

		
	return 0;
}