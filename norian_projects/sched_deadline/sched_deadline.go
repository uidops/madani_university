package main

// Javad Bajelan - 4011833206

import (
	"fmt"
	"sort"
)

type Job struct {
	Id         int
	Deadline   float64
	Efficiency float64
}

func possibility(job Job, S []Job) bool {
	new_jobs := make([]Job, len(S)+1)
	copy(new_jobs, S)
	new_jobs[len(S)] = job

	sort.Slice(new_jobs, func(i, j int) bool {
		return new_jobs[i].Deadline < new_jobs[j].Deadline
	})

	timer := 0.0
	for _, job := range new_jobs {
		if timer < job.Deadline {
			timer += 1.0
		} else {
			return false
		}
	}

	return true
}

func sched_deadline(jobs []Job) []Job {
	sort.Slice(jobs, func(i, j int) bool {
		return jobs[i].Efficiency > jobs[j].Efficiency
	})

	S := make([]Job, 0, len(jobs))

	for _, job := range jobs {
		if possibility(job, S) {
			S = append(S, job)
		}
	}

	return S
}

func main() {
	jobs := []Job{
		{1, 3, 40},
		{2, 1, 35},
		{3, 1, 30},
		{4, 3, 25},
		{5, 1, 20},
		{6, 3, 15},
		{7, 2, 10},
	}

	for _, job := range sched_deadline(jobs) {
		fmt.Printf("Job ID: %d, Deadline: %.1f, Efficiency: %.1f\n", job.Id, job.Deadline, job.Efficiency)
	}
}
