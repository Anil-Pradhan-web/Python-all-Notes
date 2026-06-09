A = [[1, 2], [3, 4]]
B = [[2, 0], [1, 2]]

sum_mat = [[A[i][j] + B[i][j] for j in range(2)] for i in range(2)]
prod_mat = [[A[i][0]*B[0][j] + A[i][1]*B[1][j] for j in range(2)] for i in range(2)]
sorted_mat = sorted(prod_mat, key=sum)

print("Sum:", sum_mat)
print("Product:", prod_mat)
print("Sorted by row sum:", sorted_mat)
