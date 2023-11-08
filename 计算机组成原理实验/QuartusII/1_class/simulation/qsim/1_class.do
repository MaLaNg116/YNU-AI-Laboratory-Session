onerror {quit -f}
vlib work
vlog -work work 1_class.vo
vlog -work work 1_class.vt
vsim -novopt -c -t 1ps -L cycloneive_ver -L altera_ver -L altera_mf_ver -L 220model_ver -L sgate work.adder_vlg_vec_tst
vcd file -direction 1_class.msim.vcd
vcd add -internal adder_vlg_vec_tst/*
vcd add -internal adder_vlg_vec_tst/i1/*
add wave /*
run -all
