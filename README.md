# Download Arxiv Papers
Python script to list or download papers from arXiv by author and/or title to the working directory. Search "Examples"
in the source code for usage. For example,

`python xdownload_papers_arxiv.py "Richardson" 5 "fortran"`

gives

```
=== arXiv PDF Downloader ===

Author Filter    : Richardson
Title Filter     : fortran
Number of PDFs   : 5

Searching arXiv with query: au:"Richardson" AND ti:"fortran"

Found 2 paper(s). Starting download...

[1] Downloading: The State of Fortran
    from: http://arxiv.org/pdf/2203.15110v2
    Saved as: richardson_the_state_of_fortran.pdf

[2] Downloading: Toward Modern Fortran Tooling and a Thriving Developer Community
    from: http://arxiv.org/pdf/2109.07382v1
    Saved as: richardson_toward_modern_fortran_tooling_and_a_thriving_developer_community.pdf

Download process completed.
```

`python xdownload_papers_arxiv.py "" 1000 "fortran"`

gives

```
=== arXiv PDF Downloader ===

Author Filter    : None
Title Filter     : fortran
Number of PDFs   : 1000

Searching arXiv with query: ti:"fortran"

Found 104 paper(s). Starting download...

[1] Downloading: Fortran2CPP: Automating Fortran-to-C++ Migration using LLMs via
  Multi-Turn Dialogue and Dual-Agent Integration
    from: http://arxiv.org/pdf/2412.19770v1
    Saved as: fortran2cpp__automating_fortran-to-c++_migration_using_llms_via_multi-turn_dialogue_and_dual-agent_integration.pdf

[2] Downloading: Portability of Fortran's `do concurrent' on GPUs
    from: http://arxiv.org/pdf/2408.07843v2
    Saved as: portability_of_fortran's_`do_concurrent'_on_gpus.pdf

[3] Downloading: Fully integrating the Flang Fortran compiler with standard MLIR
    from: http://arxiv.org/pdf/2409.18824v1
    Saved as: fully_integrating_the_flang_fortran_compiler_with_standard_mlir.pdf

[4] Downloading: Dynamic String Generation and C++-style Output in Fortran
    from: http://arxiv.org/pdf/2409.03397v1
    Saved as: dynamic_string_generation_and_c++-style_output_in_fortran.pdf

[5] Downloading: Accelerating Fortran Codes: A Method for Integrating Coarray Fortran
  with CUDA Fortran and OpenMP
    from: http://arxiv.org/pdf/2409.02294v1
    Saved as: accelerating_fortran_codes__a_method_for_integrating_coarray_fortran_with_cuda_fortran_and_openmp.pdf

[6] Downloading: StmtTree: An Easy-to-Use yet Versatile Fortran Transformation Toolkit
    from: http://arxiv.org/pdf/2407.05652v2
    Saved as: stmttree__an_easy-to-use_yet_versatile_fortran_transformation_toolkit.pdf

[7] Downloading: Evaluating AI-generated code for C++, Fortran, Go, Java, Julia, Matlab,
  Python, R, and Rust
    from: http://arxiv.org/pdf/2405.13101v2
    Saved as: evaluating_ai-generated_code_for_c++,_fortran,_go,_java,_julia,_matlab,_python,_r,_and_rust.pdf

[8] Downloading: Proof-of-concept: Using ChatGPT to Translate and Modernize an Earth
  System Model from Fortran to Python/JAX
    from: http://arxiv.org/pdf/2405.00018v1
    Saved as: proof-of-concept__using_chatgpt_to_translate_and_modernize_an_earth_system_model_from_fortran_to_python_jax.pdf

[9] Downloading: Fortran... ok, and what's next?
    from: http://arxiv.org/pdf/2402.07520v1
    Saved as: fortran..._ok,_and_what's_next.pdf

[10] Downloading: A GPU-Accelerated Modern Fortran Version of the ECHO Code for
  Relativistic Magnetohydrodynamics
    from: http://arxiv.org/pdf/2401.03008v1
    Saved as: a_gpu-accelerated_modern_fortran_version_of_the_echo_code_for_relativistic_magnetohydrodynamics.pdf

[11] Downloading: Fortran performance optimisation and auto-parallelisation by leveraging
  MLIR-based domain specific abstractions in Flang
    from: http://arxiv.org/pdf/2310.01882v1
    Saved as: fortran_performance_optimisation_and_auto-parallelisation_by_leveraging_mlir-based_domain_specific_abstractions_in_flang.pdf

[12] Downloading: Creating a Dataset for High-Performance Computing Code Translation using
  LLMs: A Bridge Between OpenMP Fortran and C++
    from: http://arxiv.org/pdf/2307.07686v4
    Saved as: creating_a_dataset_for_high-performance_computing_code_translation_using_llms__a_bridge_between_openmp_fortran_and_c++.pdf

[13] Downloading: Parsing Fortran-77 with proprietary extensions
    from: http://arxiv.org/pdf/2309.02019v1
    Saved as: parsing_fortran-77_with_proprietary_extensions.pdf

[14] Downloading: Fortran High-Level Synthesis: Reducing the barriers to accelerating HPC
  codes on FPGAs
    from: http://arxiv.org/pdf/2308.13274v1
    Saved as: fortran_high-level_synthesis__reducing_the_barriers_to_accelerating_hpc_codes_on_fpgas.pdf

[15] Downloading: Optimization and Portability of a Fusion OpenACC-based FORTRAN HPC Code
  from NVIDIA to AMD GPUs
    from: http://arxiv.org/pdf/2305.10553v1
    Saved as: optimization_and_portability_of_a_fusion_openacc-based_fortran_hpc_code_from_nvidia_to_amd_gpus.pdf

[16] Downloading: Acceleration of a production Solar MHD code with Fortran standard
  parallelism: From OpenACC to `do concurrent'
    from: http://arxiv.org/pdf/2303.03398v2
    Saved as: acceleration_of_a_production_solar_mhd_code_with_fortran_standard_parallelism__from_openacc_to_`do_concurrent'.pdf

[17] Downloading: OpenMP Fortran programs for solving the time-dependent dipolar
  Gross-Pitaevskii equation
    from: http://arxiv.org/pdf/2301.09383v1
    Saved as: openmp_fortran_programs_for_solving_the_time-dependent_dipolar_gross-pitaevskii_equation.pdf

[18] Downloading: ESFRAD. FORTRAN code for calculation of QED corrections to polarized
  ep-scattering by the electron structure function method
    from: http://arxiv.org/pdf/2212.04730v1
    Saved as: esfrad._fortran_code_for_calculation_of_qed_corrections_to_polarized_ep-scattering_by_the_electron_structure_function_method.pdf

[19] Downloading: Fortran and C programs for the time-dependent dipolar Gross-Pitaevskii
  equation in an anisotropic trap
    from: http://arxiv.org/pdf/1506.03283v3
    Saved as: fortran_and_c_programs_for_the_time-dependent_dipolar_gross-pitaevskii_equation_in_an_anisotropic_trap.pdf

[20] Downloading: Large-Scale Direct Numerical Simulations of Turbulence Using GPUs and
  Modern Fortran
    from: http://arxiv.org/pdf/2207.07098v1
    Saved as: large-scale_direct_numerical_simulations_of_turbulence_using_gpus_and_modern_fortran.pdf

[21] Downloading: The State of Fortran
    from: http://arxiv.org/pdf/2203.15110v2
    Saved as: the_state_of_fortran.pdf

[22] Downloading: Can Fortran's 'do concurrent' replace directives for accelerated
  computing?
    from: http://arxiv.org/pdf/2110.10151v1
    Saved as: can_fortran's_'do_concurrent'_replace_directives_for_accelerated_computing.pdf

[23] Downloading: Toward Modern Fortran Tooling and a Thriving Developer Community
    from: http://arxiv.org/pdf/2109.07382v1
    Saved as: toward_modern_fortran_tooling_and_a_thriving_developer_community.pdf

[24] Downloading: On the performance of GPU accelerated q-LSKUM based meshfree solvers in
  Fortran, C++, Python, and Julia
    from: http://arxiv.org/pdf/2108.07031v1
    Saved as: on_the_performance_of_gpu_accelerated_q-lskum_based_meshfree_solvers_in_fortran,_c++,_python,_and_julia.pdf

[25] Downloading: HandyG -- rapid numerical evaluation of generalised polylogarithms in
  Fortran
    from: http://arxiv.org/pdf/1909.01656v3
    Saved as: handyg_--_rapid_numerical_evaluation_of_generalised_polylogarithms_in_fortran.pdf

[26] Downloading: FORTRESS: FORTRAN programs for solving coupled Gross-Pitaevskii
  equations for spin-orbit coupled spin-1 Bose-Einstein condensate
    from: http://arxiv.org/pdf/2002.04365v2
    Saved as: fortress__fortran_programs_for_solving_coupled_gross-pitaevskii_equations_for_spin-orbit_coupled_spin-1_bose-einstein_condensate.pdf

[27] Downloading: FORTRESS II: FORTRAN programs for solving coupled Gross-Pitaevskii
  equations for spin-orbit coupled spin-2 Bose-Einstein condensate
    from: http://arxiv.org/pdf/2011.08892v1
    Saved as: fortress_ii__fortran_programs_for_solving_coupled_gross-pitaevskii_equations_for_spin-orbit_coupled_spin-2_bose-einstein_condensate.pdf

[28] Downloading: ParaMonte: A high-performance serial/parallel Monte Carlo simulation
  library for C, C++, Fortran
    from: http://arxiv.org/pdf/2009.14229v1
    Saved as: paramonte__a_high-performance_serial_parallel_monte_carlo_simulation_library_for_c,_c++,_fortran.pdf

[29] Downloading: FACt: FORTRAN toolbox for calculating fluctuations in atomic condensates
    from: http://arxiv.org/pdf/1806.01244v2
    Saved as: fact__fortran_toolbox_for_calculating_fluctuations_in_atomic_condensates.pdf

[30] Downloading: A Fortran-Keras Deep Learning Bridge for Scientific Computing
    from: http://arxiv.org/pdf/2004.10652v2
    Saved as: a_fortran-keras_deep_learning_bridge_for_scientific_computing.pdf

[31] Downloading: Targeting GPUs with OpenMP Directives on Summit: A Simple and Effective
  Fortran Experience
    from: http://arxiv.org/pdf/1812.07977v2
    Saved as: targeting_gpus_with_openmp_directives_on_summit__a_simple_and_effective_fortran_experience.pdf

[32] Downloading: C and Fortran OpenMP programs for rotating Bose-Einstein condensates
    from: http://arxiv.org/pdf/1906.06327v1
    Saved as: c_and_fortran_openmp_programs_for_rotating_bose-einstein_condensates.pdf

[33] Downloading: A parallel Fortran framework for neural networks and deep learning
    from: http://arxiv.org/pdf/1902.06714v2
    Saved as: a_parallel_fortran_framework_for_neural_networks_and_deep_learning.pdf

[34] Downloading: phq: a Fortran code to compute phonon quasiparticle properties and
  dispersions
    from: http://arxiv.org/pdf/1902.06395v1
    Saved as: phq__a_fortran_code_to_compute_phonon_quasiparticle_properties_and_dispersions.pdf

[35] Downloading: Fortran interface layer of the framework for developing particle
  simulator FDPS
    from: http://arxiv.org/pdf/1804.08935v2
    Saved as: fortran_interface_layer_of_the_framework_for_developing_particle_simulator_fdps.pdf

[36] Downloading: PyMieDAP: a Python--Fortran tool to compute fluxes and polarization
  signals of (exo)planets
    from: http://arxiv.org/pdf/1804.08357v1
    Saved as: pymiedap__a_python--fortran_tool_to_compute_fluxes_and_polarization_signals_of_(exo)planets.pdf

[37] Downloading: From MPI to MPI+OpenACC: Conversion of a legacy FORTRAN PCG solver for
  the spherical Laplace equation
    from: http://arxiv.org/pdf/1709.01126v2
    Saved as: from_mpi_to_mpi+openacc__conversion_of_a_legacy_fortran_pcg_solver_for_the_spherical_laplace_equation.pdf

[38] Downloading: On quality of implementation of Fortran 2008 complex intrinsic functions
  on branch cuts
    from: http://arxiv.org/pdf/1712.10230v1
    Saved as: on_quality_of_implementation_of_fortran_2008_complex_intrinsic_functions_on_branch_cuts.pdf

[39] Downloading: Hybrid Fortran: High Productivity GPU Porting Framework Applied to
  Japanese Weather Prediction Model
    from: http://arxiv.org/pdf/1710.08616v2
    Saved as: hybrid_fortran__high_productivity_gpu_porting_framework_applied_to_japanese_weather_prediction_model.pdf

[40] Downloading: Domain-Specific Acceleration and Auto-Parallelization of Legacy
  Scientific Code in FORTRAN 77 using Source-to-Source Compilation
    from: http://arxiv.org/pdf/1711.04471v1
    Saved as: domain-specific_acceleration_and_auto-parallelization_of_legacy_scientific_code_in_fortran_77_using_source-to-source_compilation.pdf

[41] Downloading: OpenMP GNU and Intel Fortran programs for solving the time-dependent
  Gross-Pitaevskii equation
    from: http://arxiv.org/pdf/1709.04423v1
    Saved as: openmp_gnu_and_intel_fortran_programs_for_solving_the_time-dependent_gross-pitaevskii_equation.pdf

[42] Downloading: dotCall64: An Efficient Interface to Compiled C/C++ and Fortran Code
  Supporting Long Vectors
    from: http://arxiv.org/pdf/1702.08188v1
    Saved as: dotcall64__an_efficient_interface_to_compiled_c_c++_and_fortran_code_supporting_long_vectors.pdf

[43] Downloading: RCCPAC: A parallel relativistic coupled-cluster program for closed-shell
  and one-valence atoms and ions in FORTRAN
    from: http://arxiv.org/pdf/1612.08331v2
    Saved as: rccpac__a_parallel_relativistic_coupled-cluster_program_for_closed-shell_and_one-valence_atoms_and_ions_in_fortran.pdf

[44] Downloading: Collier: a fortran-based Complex One-Loop LIbrary in Extended
  Regularizations
    from: http://arxiv.org/pdf/1604.06792v2
    Saved as: collier__a_fortran-based_complex_one-loop_library_in_extended_regularizations.pdf

[45] Downloading: OpenMP Fortran and C programs for solving the time-dependent
  Gross-Pitaevskii equation in an anisotropic trap
    from: http://arxiv.org/pdf/1605.03958v1
    Saved as: openmp_fortran_and_c_programs_for_solving_the_time-dependent_gross-pitaevskii_equation_in_an_anisotropic_trap.pdf

[46] Downloading: Fortran code for generating random probability vectors, unitaries, and
  quantum states
    from: http://arxiv.org/pdf/1512.05173v2
    Saved as: fortran_code_for_generating_random_probability_vectors,_unitaries,_and_quantum_states.pdf

[47] Downloading: Implementation of the Spherical Coordinate Representation of Protein 3D
  Structures and its Applications Using FORTRAN 77/90 Language
    from: http://arxiv.org/pdf/1512.00424v1
    Saved as: implementation_of_the_spherical_coordinate_representation_of_protein_3d_structures_and_its_applications_using_fortran_77_90_language.pdf

[48] Downloading: Implementation of the Tangent Sphere and Cutting Plane Methods in the
  Quantitative Determination of Ligand Binding Site Burial Depths in Proteins
  Using FORTRAN 77/90 Language
    from: http://arxiv.org/pdf/1512.00423v1
    Saved as: implementation_of_the_tangent_sphere_and_cutting_plane_methods_in_the_quantitative_determination_of_ligand_binding_site_burial_depths_in_proteins_using_fortran_77_90_language.pdf

[49] Downloading: Implementation of The Double-Centroid Reduced Representation of Proteins
  and its Application to the Prediction of Ligand Binding Sites and
  Protein-Protein Interaction Partners Using FORTRAN 77/90 Language
    from: http://arxiv.org/pdf/1512.00003v1
    Saved as: implementation_of_the_double-centroid_reduced_representation_of_proteins_and_its_application_to_the_prediction_of_ligand_binding_sites_and_protein-protein_interaction_partners_using_fortran_77_90_language.pdf

[50] Downloading: anQCD: Fortran programs for couplings at complex momenta in various
  analytic QCD models
    from: http://arxiv.org/pdf/1506.07201v1
    Saved as: anqcd__fortran_programs_for_couplings_at_complex_momenta_in_various_analytic_qcd_models.pdf

[51] Downloading: Remark on "Algorithm 916: Computing the Faddeyeva and Voigt functions":
  Efficiency Improvements and Fortran Translation
    from: http://arxiv.org/pdf/1505.06848v1
    Saved as: remark_on__algorithm_916__computing_the_faddeyeva_and_voigt_functions___efficiency_improvements_and_fortran_translation.pdf

[52] Downloading: Loo.py: From Fortran to performance via transformation and substitution
  rules
    from: http://arxiv.org/pdf/1503.07659v2
    Saved as: loo.py__from_fortran_to_performance_via_transformation_and_substitution_rules.pdf

[53] Downloading: Mathematica and Fortran programs for various analytic QCD couplings
    from: http://arxiv.org/pdf/1411.1581v1
    Saved as: mathematica_and_fortran_programs_for_various_analytic_qcd_couplings.pdf

[54] Downloading: COLLIER -- A fortran-library for one-loop integrals
    from: http://arxiv.org/pdf/1407.0087v1
    Saved as: collier_--_a_fortran-library_for_one-loop_integrals.pdf

[55] Downloading: Is Fortran Still Relevant? Comparing Fortran with Java and C++
    from: http://arxiv.org/pdf/1407.2190v1
    Saved as: is_fortran_still_relevant__comparing_fortran_with_java_and_c++.pdf

[56] Downloading: FDCHQHP:A Fortran Package for Heavy Quarkonium HadroProduction
    from: http://arxiv.org/pdf/1405.2143v1
    Saved as: fdchqhp_a_fortran_package_for_heavy_quarkonium_hadroproduction.pdf

[57] Downloading: RNGSSELIB: Program library for random number generation. More
  generators, parallel streams of random numbers and Fortran compatibility
    from: http://arxiv.org/pdf/1307.5866v1
    Saved as: rngsselib__program_library_for_random_number_generation._more_generators,_parallel_streams_of_random_numbers_and_fortran_compatibility.pdf

[58] Downloading: An improved algorithm and a Fortran 90 module for computing the conical
  function $P^m_{-1/2+iτ}(x)$
    from: http://arxiv.org/pdf/1306.0231v1
    Saved as: an_improved_algorithm_and_a_fortran_90_module_for_computing_the_conical_function_$p^m_{-1_2+iτ}(x)$.pdf

[59] Downloading: Object-oriented implementations of the MPDATA advection equation solver
  in C++, Python and Fortran
    from: http://arxiv.org/pdf/1301.1334v2
    Saved as: object-oriented_implementations_of_the_mpdata_advection_equation_solver_in_c++,_python_and_fortran.pdf

[60] Downloading: Performance of FORTRAN and C GPU Extensions for a Benchmark Suite of
  Fourier Pseudospectral Algorithms
    from: http://arxiv.org/pdf/1206.3215v2
    Saved as: performance_of_fortran_and_c_gpu_extensions_for_a_benchmark_suite_of_fourier_pseudospectral_algorithms.pdf

[61] Downloading: Programing Using High Level Design With Python and FORTRAN: A Study Case
  in Astrophysics
    from: http://arxiv.org/pdf/1207.3658v1
    Saved as: programing_using_high_level_design_with_python_and_fortran__a_study_case_in_astrophysics.pdf

[62] Downloading: A High-Performance Fortran Code to Calculate Spin- and Parity-Dependent
  Nuclear Level Densities
    from: http://arxiv.org/pdf/1206.4583v1
    Saved as: a_high-performance_fortran_code_to_calculate_spin-_and_parity-dependent_nuclear_level_densities.pdf

[63] Downloading: AD in Fortran, Part 2: Implementation via Prepreprocessor
    from: http://arxiv.org/pdf/1203.1450v2
    Saved as: ad_in_fortran,_part_2__implementation_via_prepreprocessor.pdf

[64] Downloading: AD in Fortran, Part 1: Design
    from: http://arxiv.org/pdf/1203.1448v2
    Saved as: ad_in_fortran,_part_1__design.pdf

[65] Downloading: A Fortran 90 Hartree-Fock program for one-dimensional periodic
  $π$-conjugated systems using Pariser-Parr-Pople model
    from: http://arxiv.org/pdf/1108.5896v1
    Saved as: a_fortran_90_hartree-fock_program_for_one-dimensional_periodic_$π$-conjugated_systems_using_pariser-parr-pople_model.pdf

[66] Downloading: ForOpenCL: Transformations Exploiting Array Syntax in Fortran for
  Accelerator Programming
    from: http://arxiv.org/pdf/1107.2157v1
    Saved as: foropencl__transformations_exploiting_array_syntax_in_fortran_for_accelerator_programming.pdf

[67] Downloading: QCDMAPT_F: Fortran version of QCDMAPT package
    from: http://arxiv.org/pdf/1107.1045v1
    Saved as: qcdmapt_f__fortran_version_of_qcdmapt_package.pdf

[68] Downloading: CHAPLIN - Complex Harmonic Polylogarithms in Fortran
    from: http://arxiv.org/pdf/1106.5739v1
    Saved as: chaplin_-_complex_harmonic_polylogarithms_in_fortran.pdf

[69] Downloading: NMSDECAY: A Fortran Code for Supersymmetric Particle Decays in the
  Next-to-Minimal Supersymmetric Standard Model
    from: http://arxiv.org/pdf/1106.5633v1
    Saved as: nmsdecay__a_fortran_code_for_supersymmetric_particle_decays_in_the_next-to-minimal_supersymmetric_standard_model.pdf

[70] Downloading: SusyBSG: a fortran code for BR[B -> Xs gamma] in the MSSM with Minimal
  Flavor Violation
    from: http://arxiv.org/pdf/0712.3265v3
    Saved as: susybsg__a_fortran_code_for_br[b_-__xs_gamma]_in_the_mssm_with_minimal_flavor_violation.pdf

[71] Downloading: Fortran programs for the time-dependent Gross-Pitaevskii equation in a
  fully anisotropic trap
    from: http://arxiv.org/pdf/0904.3131v4
    Saved as: fortran_programs_for_the_time-dependent_gross-pitaevskii_equation_in_a_fully_anisotropic_trap.pdf

[72] Downloading: A general purpose Fortran 90 electronic structure program for conjugated
  systems using Pariser-Parr-Pople model
    from: http://arxiv.org/pdf/0912.4576v1
    Saved as: a_general_purpose_fortran_90_electronic_structure_program_for_conjugated_systems_using_pariser-parr-pople_model.pdf

[73] Downloading: TaylUR 3, a multivariate arbitrary-order automatic differentiation
  package for Fortran 95
    from: http://arxiv.org/pdf/0910.5111v2
    Saved as: taylur_3,_a_multivariate_arbitrary-order_automatic_differentiation_package_for_fortran_95.pdf

[74] Downloading: A chiral lagrangian with broken scale: a Fortran code with the thermal
  contributions of the dilaton field
    from: http://arxiv.org/pdf/0909.0924v1
    Saved as: a_chiral_lagrangian_with_broken_scale__a_fortran_code_with_the_thermal_contributions_of_the_dilaton_field.pdf

[75] Downloading: A FORTRAN coded regular expression Compiler for IBM 1130 Computing
  System
    from: http://arxiv.org/pdf/0905.0740v1
    Saved as: a_fortran_coded_regular_expression_compiler_for_ibm_1130_computing_system.pdf

[76] Downloading: Fortran MPI Checkerboard Code for SU(3) Lattice Gauge Theory II
    from: http://arxiv.org/pdf/0904.1179v1
    Saved as: fortran_mpi_checkerboard_code_for_su(3)_lattice_gauge_theory_ii.pdf

[77] Downloading: Fortran MPI Checkerboard Code for SU(3) Lattice Gauge Theory I
    from: http://arxiv.org/pdf/0904.0642v1
    Saved as: fortran_mpi_checkerboard_code_for_su(3)_lattice_gauge_theory_i.pdf

[78] Downloading: Fortran 90 implementation of the Hartree-Fock approach within the CNDO/2
  and INDO models
    from: http://arxiv.org/pdf/0812.3690v1
    Saved as: fortran_90_implementation_of_the_hartree-fock_approach_within_the_cndo_2_and_indo_models.pdf

[79] Downloading: A Fortran 90 program to solve the Hartree-Fock equations for interacting
  spin-1/2 Fermions confined in Harmonic potentials
    from: http://arxiv.org/pdf/0807.3444v1
    Saved as: a_fortran_90_program_to_solve_the_hartree-fock_equations_for_interacting_spin-1_2_fermions_confined_in_harmonic_potentials.pdf

[80] Downloading: New version announcement for TaylUR, an arbitrary-order diagonal
  automatic differentiation package for Fortran 95
    from: http://arxiv.org/pdf/0704.0274v1
    Saved as: new_version_announcement_for_taylur,_an_arbitrary-order_diagonal_automatic_differentiation_package_for_fortran_95.pdf

[81] Downloading: NMSPEC: A Fortran code for the sparticle and Higgs masses in the NMSSM
  with GUT scale boundary conditions
    from: http://arxiv.org/pdf/hep-ph/0612134v1
    Saved as: nmspec__a_fortran_code_for_the_sparticle_and_higgs_masses_in_the_nmssm_with_gut_scale_boundary_conditions.pdf

[82] Downloading: A FORTRAN code for $γγ\to Z Z $ in SM and MSSM
    from: http://arxiv.org/pdf/hep-ph/0610085v2
    Saved as: a_fortran_code_for_$γγ_to_z_z_$_in_sm_and_mssm.pdf

[83] Downloading: A basis-set based Fortran program to solve the Gross-Pitaevskii Equation
  for dilute Bose gases in harmonic and anharmonic traps
    from: http://arxiv.org/pdf/cond-mat/0603732v1
    Saved as: a_basis-set_based_fortran_program_to_solve_the_gross-pitaevskii_equation_for_dilute_bose_gases_in_harmonic_and_anharmonic_traps.pdf

[84] Downloading: f2mma: FORTRAN to Mathematica translator
    from: http://arxiv.org/pdf/cs/0507054v4
    Saved as: f2mma__fortran_to_mathematica_translator.pdf

[85] Downloading: TaylUR, an arbitrary-order diagonal automatic differentiation package
  for Fortran 95
    from: http://arxiv.org/pdf/physics/0506222v2
    Saved as: taylur,_an_arbitrary-order_diagonal_automatic_differentiation_package_for_fortran_95.pdf

[86] Downloading: SuSpect: a Fortran Code for the Supersymmetric and Higgs Particle
  Spectrum in the MSSM
    from: http://arxiv.org/pdf/hep-ph/0211331v2
    Saved as: suspect__a_fortran_code_for_the_supersymmetric_and_higgs_particle_spectrum_in_the_mssm.pdf

[87] Downloading: NMHDECAY: A Fortran Code for the Higgs Masses, Couplings and Decay
  Widths in the NMSSM
    from: http://arxiv.org/pdf/hep-ph/0406215v3
    Saved as: nmhdecay__a_fortran_code_for_the_higgs_masses,_couplings_and_decay_widths_in_the_nmssm.pdf

[88] Downloading: ADF95: Tool for automatic differentiation of a FORTRAN code designed for
  large numbers of independent variables
    from: http://arxiv.org/pdf/cs/0503014v1
    Saved as: adf95__tool_for_automatic_differentiation_of_a_fortran_code_designed_for_large_numbers_of_independent_variables.pdf

[89] Downloading: SDECAY - A Fortran Code for SUSY Particle Decays in the MSSM
    from: http://arxiv.org/pdf/hep-ph/0409200v1
    Saved as: sdecay_-_a_fortran_code_for_susy_particle_decays_in_the_mssm.pdf

[90] Downloading: KDTREE 2: Fortran 95 and C++ software to efficiently search for near
  neighbors in a multi-dimensional Euclidean space
    from: http://arxiv.org/pdf/physics/0408067v2
    Saved as: kdtree_2__fortran_95_and_c++_software_to_efficiently_search_for_near_neighbors_in_a_multi-dimensional_euclidean_space.pdf

[91] Downloading: SDECAY: a Fortran code for the decays of the supersymmetric particles in
  the MSSM
    from: http://arxiv.org/pdf/hep-ph/0311167v1
    Saved as: sdecay__a_fortran_code_for_the_decays_of_the_supersymmetric_particles_in_the_mssm.pdf

[92] Downloading: FORTRAN-codes for an analysis of the ultrashort pulse propagation
    from: http://arxiv.org/pdf/physics/0306064v1
    Saved as: fortran-codes_for_an_analysis_of_the_ultrashort_pulse_propagation.pdf

[93] Downloading: A Fortran Code for Null Geodesic Solutions in the Lemaitre-Tolman-Bondi
  Spacetime
    from: http://arxiv.org/pdf/gr-qc/0205095v1
    Saved as: a_fortran_code_for_null_geodesic_solutions_in_the_lemaitre-tolman-bondi_spacetime.pdf

[94] Downloading: The general harmonic-oscillator brackets: compact expression,
  symmetries, sums and Fortran code
    from: http://arxiv.org/pdf/nucl-th/0105009v1
    Saved as: the_general_harmonic-oscillator_brackets__compact_expression,_symmetries,_sums_and_fortran_code.pdf

[95] Downloading: Object-oriented construction of a multigrid electronic-structure code
  with Fortran 90
    from: http://arxiv.org/pdf/physics/9911031v1
    Saved as: object-oriented_construction_of_a_multigrid_electronic-structure_code_with_fortran_90.pdf

[96] Downloading: The recursive adaptive quadrature in MS Fortran-77
    from: http://arxiv.org/pdf/physics/9905035v2
    Saved as: the_recursive_adaptive_quadrature_in_ms_fortran-77.pdf

[97] Downloading: POLRAD 2.0. FORTRAN code for the Radiative Corrections Calculation to
  Deep Inelastic Scattering of Polarized Particles
    from: http://arxiv.org/pdf/hep-ph/9706516v1
    Saved as: polrad_2.0._fortran_code_for_the_radiative_corrections_calculation_to_deep_inelastic_scattering_of_polarized_particles.pdf

[98] Downloading: QCDF90: Lattice QCD with Fortran 90
    from: http://arxiv.org/pdf/hep-lat/9612015v1
    Saved as: qcdf90__lattice_qcd_with_fortran_90.pdf

[99] Downloading: QCDF90: A set of Fortran 90 modules for a high-level, efficient
  implementation of QCD simulations
    from: http://arxiv.org/pdf/hep-lat/9605012v4
    Saved as: qcdf90__a_set_of_fortran_90_modules_for_a_high-level,_efficient_implementation_of_qcd_simulations.pdf

[100] Downloading: The Taming of QCD by Fortran 90
    from: http://arxiv.org/pdf/hep-lat/9607027v1
    Saved as: the_taming_of_qcd_by_fortran_90.pdf

[101] Downloading: GENTLE/4fan - A package of Fortran programs for the description of e+ e-
  annihilation into four fermions
    from: http://arxiv.org/pdf/hep-ph/9603438v1
    Saved as: gentle_4fan_-_a_package_of_fortran_programs_for_the_description_of_e+_e-_annihilation_into_four_fermions.pdf

[102] Downloading: FORTRAN program for a numerical solution of the nonsinglet
  Altarelli-Parisi equation
    from: http://arxiv.org/pdf/hep-ph/9409289v1
    Saved as: fortran_program_for_a_numerical_solution_of_the_nonsinglet_altarelli-parisi_equation.pdf

[103] Downloading: A combined mathematica--fortran program package for analytical
  calculation of the matrix elements of the microscopic cluster model
    from: http://arxiv.org/pdf/nucl-th/9309011v1
    Saved as: a_combined_mathematica--fortran_program_package_for_analytical_calculation_of_the_matrix_elements_of_the_microscopic_cluster_model.pdf

[104] Downloading: An Interactive NeXTstep Interface to a Fortran Code for Solving Coupled
  Differential Equations
    from: http://arxiv.org/pdf/nucl-th/9210001v2
    Saved as: an_interactive_nextstep_interface_to_a_fortran_code_for_solving_coupled_differential_equations.pdf
```
