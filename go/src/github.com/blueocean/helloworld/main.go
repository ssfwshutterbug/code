package main

import (
	"fmt"
	"math"
)

func sum(a, b int) int {
	return a + b
}

func reverse_string(a string, b string) (string, string) {
	return b, a
}

func main() {
	fmt.Println(1, 2)
	fmt.Println(reverse_string("hello", "world"))

	var nums [3]int
	nums[0] = 0
	nums[1] = 1
	fmt.Println(nums)
	nums[0] = 1000
	fmt.Println(nums)

	var ages = [10]int{1, 2}
	fmt.Println(ages)

	apple := [10]int{1, 2}
	fmt.Println(apple)

	var counts = []float32{3, 4}
	fmt.Println(counts)

	counts = append(counts, math.Pi)
	fmt.Println(counts)
}
