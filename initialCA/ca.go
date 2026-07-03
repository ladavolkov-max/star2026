package main

import (
	"bufio"
	"flag"
	"fmt"
	"math"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"time"
)

type transition struct {
	source *state
	dest *state
	sym int
	C float32
	P[] float32
	cond bool
	temp bool
}

type state struct {
	stnum int
	δ[] *transition
	rew, pun bool
	next *state
}

type exp struct {
	t1, t2 *transition
	E float32
	next *exp
}

type marker struct {
	t *transition
	sym int
	next *marker
}

var α float32
var β float32
var γ float32
var η float32
var ζ float32
var ν float32
var κ float32

var nΣ int
var nΔ int
var c *state
var q_a *state
var t_m1 *transition
var o_l int
var o int
var so float32
var I_l []float32
var Q *state
var E *exp
var marked *marker
var nstate int
var debug bool

func main() {
	flag.Usage = func() {
		fmt.Fprintf(flag.CommandLine.Output(), "%s [flags] config\n", os.Args[0])
		flag.PrintDefaults()
	}
	flag.BoolVar(&debug, "d", false, "turn on debugging output")
	flag.Parse()
	if flag.Arg(0) == "" {
		flag.Usage()
	}
	procconfig(flag.Arg(0))
	if debug {
		dump()
	}
	now := time.Now()
	rand.Seed(now.UnixNano())
	for c = Q; c != nil; c = c.next {
		if c.stnum == 0 {
			break
		}
	}
	q_a = c
	t_m1 = nil
	o = 0
	o_l = 0
	I_l = make([]float32, nΣ, nΣ)
	marked = nil
	br := bufio.NewReader(os.Stdin)
	for {
		inline, err := br.ReadString('\n')
		if err != nil {
			break
		}
		if inline[0] == 'D' {
			dump()
		} else {
			i := parseinput(inline)
			step(i)
			fmt.Println(o, so)
		}
	}
	fmt.Fprintln(os.Stderr, nstate, "states")
}

func procconfig(cf string) {
	var nq int
	var qs, qd *state
	var f []string

	fd, err := os.Open(cf)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	bc := bufio.NewReader(fd)
	/*
	 * Learning parameters
	 */
	s, _ := bc.ReadString('\n')
	fmt.Sscan(s, &α)
	s, _ = bc.ReadString('\n')
	fmt.Sscan(s, &β)
	s, _ = bc.ReadString('\n')
	fmt.Sscan(s, &γ)
	s, _ = bc.ReadString('\n')
	fmt.Sscan(s, &η)
	s, _ = bc.ReadString('\n')
	fmt.Sscan(s, &ζ)
	s, _ = bc.ReadString('\n')
	fmt.Sscan(s, &ν)
	s, _ = bc.ReadString('\n')
	fmt.Sscan(s, &κ)
	/*
	 * Number of initial states
	 */
	s, _ = bc.ReadString('\n')
	fmt.Sscan(s, &nq)
	/*
	 * Size of input alphabet
	 */
	s, _ = bc.ReadString('\n')
	fmt.Sscan(s, &nΣ)
	/*
	 * Size of outut alphabet
	 */
	s, _ = bc.ReadString('\n')
	fmt.Sscan(s, &nΔ)
	for i := 0; i < nq; i++ {
		mkstate()
	}
	if debug {
		fmt.Println("alpha =", α)
		fmt.Println("beta =", β)
		fmt.Println("gamma =", γ)
		fmt.Println("eta =", η)
		fmt.Println("zeta =", ζ)
		fmt.Println("nu =", ν)
		fmt.Println("kappa =", κ)
		fmt.Println("nQ =", nq)
		fmt.Println("nsigma =", nΣ)
		fmt.Println("ndelta =", nΔ)
	}
	/*
	 * Set of reward states
	 */
	s, _ = bc.ReadString('\n')
	st := strings.TrimSpace(s)
	if len(st) > 0 {
		f = strings.Split(st, " ")
		for _, q := range f {
			qn, _ := strconv.Atoi(q)
			for qs = Q; qs != nil && qs.stnum != qn; qs = qs.next { }
			qs.rew = true
		}
	}
	/*
	 * Set of punishment states
	 */
	s, _ = bc.ReadString('\n')
	st = strings.TrimSpace(s)
	if len(st) > 0 {
		f = strings.Split(strings.TrimSpace(s), " ")
		for _, q := range f {
			qn, _ := strconv.Atoi(q)
			for qs = Q; qs != nil && qs.stnum != qn; qs = qs.next { }
			qs.pun = true
		}
	}
	/*
	 * Set of transitions
	 */
	for {
		s, err = bc.ReadString('\n')
		if err != nil {
			break
		}
		t := new(transition)
		f = strings.Split(strings.TrimSpace(s), " ")
		src, _ := strconv.Atoi(f[0])
		dst, _ := strconv.Atoi(f[1])
		sym, _ := strconv.Atoi(f[2])
		c, _ := strconv.ParseFloat(f[3], 32)
		for qs = Q; qs != nil && qs.stnum != src; qs = qs.next { }
		for qd = Q; qd != nil && qd.stnum != dst; qd = qd.next { }
		t.source = qs
		t.dest = qd
		t.sym = sym
		t.C = float32(c)
		t.P = make([]float32, nΔ, nΔ)
		qs.δ[sym] = t
		for i := 4; i < len(f); i += 2 {
			sym, _ = strconv.Atoi(f[i])
			prob, _ := strconv.ParseFloat(f[i+1], 32)
			t.P[sym] = float32(prob)
		}
	}
}

func parseinput(s string) []float32 {
	var sym int
	var str float32

	i := make([]float32, nΣ, nΣ)
	inlist := strings.Split(s, " ")
	for _, inp := range inlist {
		fmt.Sscanf(inp, "%d/%f", &sym, &str)
		if debug {
			fmt.Println("input ", sym, "with strength", str)
		}
		i[sym] = str
	}	
	return i
}

func dump() {
	dumpmach(Q)
	for e := E; e != nil; e = e.next {
		if e.t1 == nil || e.t2 == nil {
			fmt.Fprintln(os.Stderr, "nil pointer in E", e.t1, e.t2)
		}
		fmt.Fprint(os.Stderr, "E(", e.t1.source.stnum, ",", e.t1.sym, ",",
			e.t2.source.stnum, ",", e.t2.sym, ") = ", e.E, "\n")
	}
}

func dumpmach(q *state) {
	if q == nil {
		return
	}
	dumpmach(q.next)
	fmt.Fprintln(os.Stderr, "q", q.stnum, "  R:", q.rew, "   P:", q.pun)
	for a := 0; a < nΣ; a++ {
		t := q.δ[a]
		if t != nil {
			fmt.Fprintln(os.Stderr, "\tdelta(", q.stnum, ",", a, ")=", t.dest.stnum,
				"C:", t.C, " cond:", t.cond, " temp:", t.temp)
			fmt.Fprint(os.Stderr, "\t\tP: ")
			for b := 0; b < nΔ; b++ {
				fmt.Fprint(os.Stderr, t.P[b], " ")
			}
			fmt.Fprintln(os.Stderr)
		}
	}
}

func step(I []float32) {
	if I[0] > 0.0001 {
		t := c.δ[0]
		if t != nil {
			t.temp = false
			c = t.dest
		}
		q_a = c
		o_l = o
		o = 0
		app_cond(0, 1.0)
		marked = nil
		t_m1 = nil
		I_l = make([]float32, nΣ, nΣ)
		return
	}
	a_d := 0
	s_d := float32(0.0)
	for a := 0; a < nΣ; a++ {
		if I[a] > s_d {
			a_d = a
			s_d = I[a]
		}
	}
	if s_d <= 0.0001 {
		fmt.Fprintln(os.Stderr, "Invalid input: strength too small")
		return
	}
	createt(I)
	t := c.δ[a_d]
	o_l = o
	o = λ(t)
	so = s_d * t.C / (1.0 + t.C)
	updateE(I, a_d)
	if t.dest.rew {
		reward(s_d)
	} else if t.dest.pun {
		punish(s_d)
	} else if o_l != 0 && o != o_l {
		app_cond(a_d, s_d)
	}
	c = t.dest
	I_l = I
	t_m1 = t
}

func createt(I []float32) {
	if c.δ[0] != nil && c.δ[0].temp {
		c.δ[0] = nil
	}
	for i := 1; i < nΣ; i++ {
		if I[i] > 0.0001 {
			if c.δ[i] == nil {
				qn := mkstate()
				qp := lookuptrans(i)
				c.δ[i] = mktrans(c, qn, i, 0.1, false)
				qn.δ[0] = mktrans(qn, q_a, 0, 1.0, true)
				qn.δ[0].P[0] = 1.0
				if qp != nil {
					copy(c.δ[i].P[:], qp.δ[i].P[:])
					c.δ[i].C = qp.δ[i].C
					qn.rew = qp.δ[i].dest.rew
					qn.pun = qp.δ[i].dest.pun
					e := new(exp)
					e.t1 = c.δ[i]
					e.t2 = qp.δ[i]
					e.next = E
					E = e
					e = new(exp)
					e.t1 = qp.δ[i]
					e.t2 = c.δ[i]
					e.next = E
					E = e
				} else {
					c.δ[i].P[0] = η
					x := (1.0 - η) / float32(nΔ - 1)
					for b := 1; b < nΔ; b++ {
						c.δ[i].P[b] = x
					}
				}
			}
		}
	}
}

func updateE(I []float32, a_d int) {
	var e *exp

	if t_m1 != nil {
		q_l := t_m1.source
		a_l := t_m1.sym
		e = findE(q_l, a_l, c, a_d)
		if e != nil {
			ΔE := α * (1.0 - e.E)
			e.E += ΔE
			q_l.δ[a_l].C *= 1.0 - β * abs32(ΔE)
			e = findE(c, a_d, q_l, a_l)
			ΔE = α * (1.0 - e.E)
			e.E += ΔE
			c.δ[a_d].C *= 1.0 - β * abs32(ΔE)
		} else if a_l != 0 {
			e = new(exp)
			e.t1 = q_l.δ[a_l]
			e.t2 = c.δ[a_d]
			e.E = α
			e.next = E
			E = e
			e = new(exp)
			e.t1 = c.δ[a_d]
			e.t2 = q_l.δ[a_l]
			e.E = α
			e.next = E
			E = e
			if debug {
				fmt.Printf("Creating E(%d,%d,%d,%d)\n",
					q_l.stnum, a_l, c.stnum, a_d)
			}
		}
		for a := 1; a < nΣ; a++ {
			if I[a] < 0.0001 {
				e = findE(q_l, a_l, c, a)
				if e != nil {
					ΔE := -α * e.E
					e.E += ΔE
					q_l.δ[a_l].C *= 1.0 - β * abs32(ΔE)
					e = findE(c, a, q_l, a_l)
					ΔE = -α * e.E
					e.E += ΔE
					c.δ[a].C *= 1.0 - β * abs32(ΔE)
				}
			}
		}
		for q := Q; q != nil; q = q.next {
			for a := 1; a < nΣ; a++ {
				if (q != q_l || a != a_l) && q.δ[a] != nil {
					e = findE(c, a_d, q, a)
					if e != nil {
						ΔE := -α * e.E
						e.E += ΔE
						c.δ[a_d].C *= 1.0 - β * abs32(ΔE)
						e = findE(q, a, c, a_d)
						ΔE = -α * e.E
						e.E += ΔE
						q.δ[a].C *= 1.0 - β * abs32(ΔE)
					}
				}
			}
		}
	}
	for a := 1; a < nΣ; a++ {
		for b := 1; b < nΣ; b++ {
			if a != b {
				if I[a] > 0.0001 && I[b] > 0.0001 {
					e = findE(c, a, c, b)
					if e != nil {
						ΔE := α * (1.0 - e.E)
						e.E += ΔE
						c.δ[a].C *= 1.0 - β * abs32(ΔE)
					} else {
						if c.δ[a] != nil && c.δ[b] != nil {
							e = new(exp)
							e.t1 = c.δ[a]
							e.t2 = c.δ[b]
							e.E = α
							e.next = E
							E = e
						}
					}
				} else if I[a] > 0.0001 || I[b] > 0.0001 {
					e = findE(c, a, c, b)
					if e != nil {
						ΔE := -α * e.E
						e.E += ΔE
						c.δ[a].C *= 1.0 - β * abs32(ΔE)
					}
				}
			} 
		}
	}
}

func reward(s_d float32) {
	t := float32(1.0)
	for m := marked; m != nil; m = m.next {
		x := (ζ * t * s_d) / m.t.C
		for b := 0; b < nΔ; b++ {
			if b == m.sym {
				m.t.P[b] = (m.t.P[b] + x) / (1.0 + x)
			} else {
				m.t.P[b] /= 1.0 + x
			}
		}
		m.t.C += ζ * t * s_d
		for qp := Q; qp != nil; qp = qp.next {
			if qp != m.t.source && qp.δ[m.t.sym] != nil {
				x = (ν * ζ * t * s_d) / qp.δ[m.t.sym].C
				for b := 0; b < nΔ; b++ {
					if b == m.sym {
						qp.δ[m.t.sym].P[b] = (qp.δ[m.t.sym].P[b] + x) / (1.0 + x)
					} else {
						qp.δ[m.t.sym].P[b] /= 1.0 + x
					}
				}
				qp.δ[m.t.sym].C += ν * ζ * t * s_d
			}
		}
		t *= κ
	}
	marked = nil
}

func punish(s_d float32) {
	t := float32(1.0)
	for m := marked; m != nil; m = m.next {
		x := (ζ * t * s_d) / m.t.C
		y := x / float32(nΔ -1)
		for b := 0; b < nΔ; b++ {
			if b == m.sym {
				m.t.P[b] /= 1.0 + x
			} else {
				m.t.P[b] = (m.t.P[b] + y) / (1.0 + x)
			}
		}
		m.t.C += ζ * t * s_d
		for qp := Q; qp != nil; qp = qp.next {
			if qp != m.t.source && qp.δ[m.t.sym] != nil {
				x = (ν * ζ * t * s_d) / qp.δ[m.t.sym].C
				y = x / float32(nΔ - 1)
				for b := 0; b < nΔ; b++ {
					if b == m.sym {
						qp.δ[m.t.sym].P[b] /= 1.0 + x
					} else {
						qp.δ[m.t.sym].P[b] = (qp.δ[m.t.sym].P[b] + y) / (1.0 + x)
					}
				}
				qp.δ[m.t.sym].C += ν * ζ * t * s_d
			}
		}
		t *= κ
	}
	marked = nil
}

func app_cond(a_d int, s_d float32) {
	if t_m1 == nil {
		return
	}
	q_l := t_m1.source
	a_l := t_m1.sym
	if debug {
		fmt.Fprint(os.Stderr, "Conditioning: c=", c.stnum, " a_d=", a_d,
			" q_l=", q_l.stnum, " a_l=", a_l, " o_l=", o_l, " I_l=", I_l, "\n")
	}
	for q := Q; q != nil; q = q.next {
		for a := 1; a < nΣ; a++ {
			if q.δ[a] != nil {
				q.δ[a].cond = false
			}
		}
	}
	for a := 1; a < nΣ; a++ {
		if I_l[a] > 0.0001 && q_l.δ[a] != nil {
			e := findE(q_l, a_l, q_l, a)
			if e != nil {
				for b := 0; b < nΔ; b++ {
					if b == o_l {
						q_l.δ[a].P[b] = incprob(q_l, a, s_d, b)
					} else {
						q_l.δ[a].P[b] = decprob(q_l, a, s_d, b)
					}
				}
			}
		}
	}
	for q := Q; q != nil; q = q.next {
		for a := 1; a < nΣ; a++ {
			if q.δ[a] != nil && q.δ[a].dest == q_l {
				e := findE(q_l, a_l, q, a)
				if e != nil {
					for b := 0; b < nΔ; b++ {
						if b == o_l {
							q.δ[a].P[b] = incprob(q, a, s_d, b)
						} else {
							q.δ[a].P[b] = decprob(q, a, s_d, b)
						}
					}
				}
			}
		}
	}
	for a := 1; a < nΣ; a++ {
		if I_l[a] > 0.0001 && q_l.δ[a] != nil && !(q_l.δ[a].cond) {
			e := findE(q_l, a_l, q_l, a)
			if e != nil {
				if !(q_l.δ[a].cond) {
					q_l.δ[a].C += γ * s_d
					q_l.δ[a].cond = true
					updcond(q_l, a, s_d / q_l.δ[a].C)
				}
			}
		}
	}
	for q := Q; q != nil; q = q.next {
		for a := 1; a < nΣ; a++ {
			if q.δ[a] != nil && q.δ[a].dest == q_l && !(q.δ[a].cond) {
				e := findE(q_l, a_l, q, a)
				if e != nil {
					if !(q.δ[a].cond) {
						q.δ[a].C += γ * s_d
						q.δ[a].cond = true
						updcond(q, a, s_d / q.δ[a].C)
					}
				}
			}
		}
	}
}

func updcond(qp *state, ap int, s float32) {
	if s <= 0.0001 {
		return
	}
	if debug {
		fmt.Fprint(os.Stderr, "Propagating conditioning qp=", qp.stnum, " ap=", ap, "\n")
	}
	for a := 1; a < nΣ; a++ {
		if qp.δ[a] != nil && !(qp.δ[a].cond) {
			e := findE(qp, ap, qp, a)
			if e != nil {
				for b := 0; b < nΔ; b++ {
					if b == o_l {
						qp.δ[a].P[b] = incprob(qp, a, s, b)
					} else {
						qp.δ[a].P[b] = decprob(qp, a, s, b)
					}
				}
			}
		}
	}
	for q := Q; q != nil; q = q.next {
		for a := 1; a < nΣ; a++ {
			if q.δ[a] != nil && q.δ[a].dest == qp && !(q.δ[a].cond) {
				e := findE(qp, ap, q, a)
				if e != nil {
					for b := 0; b < nΔ; b++ {
						if b == o_l {
							q.δ[a].P[b] = incprob(q, a, s, b)
						} else {
							q.δ[a].P[b] = decprob(q, a, s, b)
						}
					}
				}
			}
		}
	}
	for a := 1; a < nΣ; a++ {
		if /* I_l[a] > 0.0001 && */ qp.δ[a] != nil && !(qp.δ[a].cond) {
			e := findE(qp, ap, qp, a)
			if e != nil {
				qp.δ[a].C += γ * s
				qp.δ[a].cond = true
				updcond(qp, a, s / qp.δ[a].C)
			}
		}
	}
	for q := Q; q != nil; q = q.next {
		for a := 1; a < nΣ; a++ {
			if q.δ[a] != nil && q.δ[a].dest == qp && !(q.δ[a].cond) {
				e := findE(qp, ap, q, a)
				if e != nil {
					q.δ[a].C += γ * s
					q.δ[a].cond = true
					updcond(q, a, s / q.δ[a].C)
				}
			}
		}
	}
}

func incprob(q *state, a int, s float32, o int) float32 {
	x := ( γ * s ) / q.δ[a].C
	return (q.δ[a].P[o] +  x) / (1.0 + x)
}

func decprob(q *state, a int, s float32, o int) float32 {
	x := ( γ * s ) / q.δ[a].C
	return q.δ[a].P[o] / (1.0 + x)
}

func abs32(x float32) float32 {
	return float32(math.Abs(float64(x)))
}

func findE(q1 *state, a1 int, q2 *state, a2 int) *exp {
	t1 := q1.δ[a1]
	t2 := q2.δ[a2]
	if t1 == nil || t2 == nil {
		return nil
	}
	for e := E; e != nil; e = e.next {
		if e.t1 == t1 && e.t2 == t2 {
			return e
		}
	}
	return nil
}

func mktrans(src *state, dest *state, sym int, C float32, temp bool) *transition {
	t := new(transition)
	t.source = src
	t.dest = dest
	t.sym = sym
	t.P = make([]float32, nΔ, nΔ)
	t.C = C
	t.temp = temp
	return t
}

func mkstate() *state {
	s := new(state)
	s.δ = make([]*transition, nΣ, nΣ)
	s.stnum = nstate
	nstate++
	s.next = Q
	Q = s
	return s
}

func λ(t *transition) int {
	x := rand.Float32()
	for i := 0; i < nΔ; i++ {
		if x < t.P[i] {
			m := new(marker)
			m.t = t
			m.sym = i
			m.next = marked
			marked = m
			return i
		}
		x -= t.P[i]
	}
	return 0
}

func lookuptrans(sym int) *state {
	for q := Q; q != nil; q = q.next {
		if q.δ[sym] != nil {
			return q
		}
	}
	return nil
}
