
# Testing different filtering kernel implementations

1. loop on components, then loop on main (k,j,i) and then the filtering reduction (n,m,l)
2. loop on components, then interleaving the loops (n,k,m,j,l,i)
3. loop on components, then interleaving the loops (k,n,j,m,i,l)
4. n,m,l,nc,k,j,i
5. nc,n,m,l,k,j,i
