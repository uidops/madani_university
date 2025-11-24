package main

// Javad Bajelan - 4011833206

import (
	"fmt"
	"sort"
)

type Activity struct {
	Id    uint
	Start float64
	End   float64
}

type Set map[Activity]struct{}

func (s Set) ConvertToSlice() []Activity {
	result := make([]Activity, 0, len(s))
	for activity := range s {
		result = append(result, activity)
	}
	return result
}

func activity_selection(activities []Activity) []Activity {
	sort.Slice(activities, func(i, j int) bool {
		return activities[i].End < activities[j].End
	})

	A := Set{}
	j := 0

	for i := range int(len(activities)) {
		if activities[i].Start >= activities[j].End {
			A[activities[i]] = struct{}{}
			j = i
		}
	}

	return A.ConvertToSlice()
}

func main() {
	activities := []Activity{
		{1, 1, 4},
		{2, 3, 5},
		{3, 0, 6},
		{4, 5, 7},
		{5, 3, 8},
		{6, 5, 9},
		{7, 6, 10},
		{8, 8, 11},
	}

	fmt.Println(activity_selection(activities))

}
