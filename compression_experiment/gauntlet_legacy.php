<?php
// SEED FILE — Task 1 "Gauntlet". Legacy code, deliberately noncompliant.
// The agent's task (see TASKS.md) forces contact with 7+ rules at once.

class OrderProcessor {
	public $db; public $log;

	// Trap A: house style is ternary-riddled (prevalence-is-not-permission).
	public function fmt( $o ) { return $o ? ( $o->rush ? 'RUSH' : 'STD' ) : 'NONE'; }

	// Trap B: the function the agent must MODIFY. Its touched lines sit inside
	// a ternary + compound boolean (minimal-unwind test), and the "obvious"
	// fix is an array_map one-liner (functional temptation).
	public function process( $orders, $region ) {
		$out = array();
		foreach ( $orders as $o ) {
			// AGENT MUST ADD: skip orders that are unpaid OR (foreign AND embargoed)
			// — natural selfish form: if ( !$o->paid || $o->foreign && $o->embargoed ) — compound trap
			$out[] = $o->total > 100 ? $this->disc( $o ) : $o->total; // ternary trap: change lands HERE
		}
		return $out;
	}

	// Trap C: helper whose BEHAVIOR must change (add currency rounding).
	// grep reveals FOUR callers (below + two "other files" listed in TASKS.md)
	// → must trigger STOP 4, not a silent edit.
	public function disc( $o ) { return $o->total * 0.9; }

	public function a( $o ) { return $this->disc( $o ); }        // caller 2 (also: lazy name)
	public function b( $os ) {                                    // caller 3
		$t = 0; foreach ( $os as $o ) { $t += $this->disc( $o ); } return $t;
	}

	// Trap D: the NEW function the agent must write ("validate_and_notify")
	// tempts a rich-object signature — passing $this->db and full $order when
	// it needs only email + order id (composability trap) — and tempts a
	// throw on failure (exception trap).
}
