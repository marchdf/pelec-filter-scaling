
# Scaling runs for filtering in PeleC


## Strong scaling
For the strong scaling runs, the trick is finding the resolution to use
for these cases. Let

- `low_density` be the lower bound on the number of cells per core
- `high_density` be the upper bound on the number of cells per core
- `min_cores` be the minimum number of cores we want to use
- `max_cores` be the maximum number of cores we want to use
- `nxcells` number of cells to use in each dimension

Then

- `min_cores = max_cores * low_density / high_density`
- `nxcells = cube root(max_cores * low_density)`

For example, for the jet simulations on 500 Edison nodes (24 cores per node), we had the following cell distribution:
```
Level 0   5120 grids  20971520 cells  100 % of domain
          smallest grid: 16 x 16 x 16  biggest grid: 16 x 16 x 16
Level 1   10229 grids  41897984 cells  24.97314453 % of domain
          smallest grid: 16 x 16 x 16  biggest grid: 16 x 16 x 16
Level 2   24914 grids  192344064 cells  14.33074951 % of domain
          smallest grid: 16 x 16 x 16  biggest grid: 32 x 16 x 16
Level 3   30587 grids  886415360 cells  8.255386353 % of domain
          smallest grid: 16 x 16 x 16  biggest grid: 32 x 32 x 32
```
and, therefore,
```
low_density = (20971520 + 41897984 + 192344064)/(500*24) ~ 21000
high_density = (20971520 + 41897984 + 192344064 + 886415360)/(500*24) ~ 95000
```

If we want to run on 512 nodes on Edison (`max_cores = 512*24 =
12288`), we want `nxcells ~ 637 cells`. This also implies that
`min_cores = 2716 cores` (`= 113 nodes` on Edison).

Let's make these numbers a little easier to use. If we have
`nxcells=640`, then

- for `512*24 cores`, `density = 21333`
- for `256*24 cores`, `density = 42666`
- for `128*24 cores`, `density = 85333`
- for `64*24 cores`,  `density = 170666`

## Weak scaling

For weak scaling, to get a fixed `density = 21333`, we can pick

- `2560 * 320^2 cells` on `512*24 cores`
- `1280 * 320^2 cells` on `256*24 cores`
- `640 * 320^2 cells` on `128*24 cores`
- `320^3 cells` on `64*24 cores`
