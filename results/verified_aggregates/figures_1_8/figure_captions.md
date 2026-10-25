# Draft figure captions

## J01_training_energy_distribution — Training energy distribution
Distribution of the annual total site energy target in the training split (n = 8,400).

## J02_baseline_accuracy_comparison — Baseline regression metrics
Validation and held-out test RMSE and MAE of five prespecified baseline models. The held-out test results are descriptive and were not used for hyperparameter selection.

## J03_best_baseline_actual_vs_predicted — Observed versus predicted annual energy
Held-out test observed versus predicted total annual site energy for CatBoost, selected by validation RMSE.

## J04_best_baseline_residual_diagnostics — Baseline residual diagnostics
Residual scatter and distribution of CatBoost on the held-out test data; residual = observed minus predicted.

## J05_baseline_error_by_energy_range — Performance by energy-demand range
Average absolute error of CatBoost in five observed-energy quantiles of the held-out test set. This is a descriptive post-evaluation diagnostic.

## J06_cfm_training_loss — Standard CFM learning curve
Training flow-matching objective by epoch (scaled target, unitless); do not interpret this objective as RMSE.

## J07_cfm_validation_rmse — Validation RMSE evolution
Standard CFM validation RMSE across training alongside CatBoost validation RMSE. CFM checkpoint selection uses validation RMSE only.

## J08_cfm_validation_actual_vs_predicted — CFM observed versus predicted
Observed annual total site energy versus CFM predictive-sample mean, validation split only.

## J09_cfm_interval_reliability — Uncalibrated interval reliability
Nominal versus empirical central interval coverage from 32 flow samples per building on validation data.

## J100_BDG2_three_site_prediction_bias — BDG2 measured electricity model bias
Signed prediction bias across the frozen independent three-site evaluation.

## J101_BDG2_three_site_observed_predicted — BDG2 three-site observed vs predicted
Visualization capped at 99th percentile of observed data; original uncapped predictions used for metrics.

## J102_BDG2_three_site_seed_stability — BDG2 frozen test CFM seed diagnostics
All five training seeds retained; measured electricity per-hour test performance; no test-based seed selection.

## J103_BDG2_test_worst_one_percent_SSE — Frozen-test RMSE concentration
Contribution of the highest squared-error 1% of test observations to total SSE. No outlier removal.

## J104_BDG2_test_extreme_predicted_energy — Extreme frozen-test predicted electricity
Logarithmic comparison of maximum predictions and maximum observed hourly electricity; raw metrics are not transformed.

## J105_BDG2_test_calibrated_interval_failure_direction — Frozen calibrated interval containment and failure direction
Proportion inside calibrated 90% intervals and outside on each side on the frozen independent-site test.

## J106_BDG2_test_relative_RMSE_by_site — Model RMSE relative to CatBoost across unseen sites
Site-specific RMSE change relative to CatBoost. Standard CFM omitted from graph scale because of extreme divergence; present in source CSV.

## J107_BDG2_test_three_site_calibrated_coverage — Site-specific reliability of frozen prediction intervals
Calibration coverage varies by unseen site. Three sites do not establish a population-level coverage guarantee.

## J108_BDG2_test_point_vs_interval_tradeoff — Frozen-test point prediction versus uncertainty trade-off
Observed trade-off between point RMSE and conformal interval score; neither metric alone implies universal model superiority.

## J109_crosssource_frozen_primary_RMSE_relative_change — Within-study primary RMSE contrasts against CatBoost
Comparisons are computed within each distinct target/source/holdout. They are not pooled estimates. Cairo comparison uses the earlier full residual model; other studies use prespecified no-base residual.

## J10_cfm_interval_width — CFM interval width against predicted energy
Width of each uncalibrated central 90% flow-sample interval versus the corresponding predictive mean on validation data.

## J110_crosssource_frozen_primary_interval_coverage — Frozen primary 90% interval coverage by study
Observed interval coverage of pre-frozen primary candidates across dissimilar building-energy tasks. Nominal 90% line shown for context.

## J111_BDG2_inverse_transform_tail_amplification — Inverse-target amplification potential
Mathematical effect of the previously frozen fit-only log1p target mean and SD. Upper numerical clip shown as in the original implementation; not a causal attribution.

## J112_BDG2_frozen_tail_error_concentration — Frozen three-site test squared-error concentration
For each frozen method, the worst 1% of absolute-error rows and their fraction of total squared error. All predictions unmodified; 92,356 hourly samples within only three held-out sites.

## J113_BDG2_validation_solver_step_tail_sensitivity — Paired ODE discretization sensitivity on BDG2 validation
Euler16, Euler32 and Heun32 were compared with Euler64 using the same 256 validation rows, fixed initialization, and all 15 trained models. Summary median over the five fixed seeds.

## J114_BDG2_validation_generated_log_tail_hazards — Validation inverse-target tail hazard across ODE samplers
Fraction of generated samples whose unclipped log1p(kWh) value exceeds 15; no original predictions were clipped or corrected. Five-seed median.

## J115_BDG2_validation_solver_point_RMSE_by_variant — Controlled validation-only RMSE by ODE solver and CFM variant
Median validation-slice RMSE across five frozen seeds and four solver settings. This exploratory result must not be used to retune previously evaluated held-out sites.

## J116_BDG2_validation_fit_only_probabilistic_intervalscore — BDG2 validation interval score
Fixed training data; new probabilistic baselines and frozen CFM model median over 5 seeds. Two validation sites only; exploratory.

## J117_BDG2_validation_fit_only_probabilistic_coverage — BDG2 validation raw 90% coverage
Fixed training data; new probabilistic baselines and frozen CFM model median over 5 seeds. Two validation sites only; exploratory.

## J118_BDG2_validation_fit_only_probabilistic_rmse — BDG2 validation point RMSE
Fixed training data; new probabilistic baselines and frozen CFM model median over 5 seeds. Two validation sites only; exploratory.

## J119_BDG2_validation_Moose_to_Panther_CQR_diagnostic — BDG2 split-validation CQR diagnostic
Quantile bounds calibrated using the already inspected Moose validation site, evaluated on the already inspected Panther validation site. This is development evidence only and offers no independent-site guarantee.

## J11_cfm_error_vs_uncertainty — Relationship between uncertainty and error
Absolute CFM validation point-prediction error against the width of its uncalibrated 90% predictive interval.

## J120_BDG2_exploratory_distributional_RMSE — Development validation point accuracy
Fit-only training and previously inspected 2-site validation; NGBoost restricted training budget and CFM five-seed medians.

## J121_BDG2_exploratory_distributional_CRPS — Development validation probabilistic score
Fit-only training and previously inspected 2-site validation; NGBoost restricted training budget and CFM five-seed medians.

## J122_BDG2_exploratory_distributional_raw_coverage — Raw 90% coverage (exploratory)
Fit-only training and previously inspected 2-site validation; NGBoost restricted training budget and CFM five-seed medians.

## J123_BDG2_exploratory_distributional_interval_score — Development validation interval score
Fit-only training and previously inspected 2-site validation; NGBoost restricted training budget and CFM five-seed medians.

## J124_BDG2_exploratory_distributional_error_tails — Development validation error tails
Frozen point predictions of new distributional comparators; descriptive only.

## J125_COFACTOR_locked_group_split — COFACTOR building role split
Metadata-only splits frozen before meter values were read.

## J126_COFACTOR_val_RMSE — Development point error
Development-only building-disjoint validation; CFM 3 seeds, NGBoost limited fit budget.

## J127_COFACTOR_val_CRPS — Raw probabilistic quality
Development-only building-disjoint validation; CFM 3 seeds, NGBoost limited fit budget.

## J128_COFACTOR_val_coverage — Raw interval coverage
Development-only building-disjoint validation; CFM 3 seeds, NGBoost limited fit budget.

## J129_COFACTOR_val_interval_score — Raw 90% interval score
Development-only building-disjoint validation; CFM 3 seeds, NGBoost limited fit budget.

## J12_validation_catboost_vs_cfm — Point prediction: CatBoost versus CFM
Validation RMSE and MAE comparing CatBoost with Standard CFM. This does not compare predictive-distribution quality since CatBoost lacks distributional outputs.

## J130_COFACTOR_val_building_heterogeneity — Cross-building validation heterogeneity
Only the 6 development validation buildings; final test remains unopened.

## J131_COFACTOR_TEST_raw_CRPS — Locked test raw probabilistic scores
9 CFM model/seed combinations and NGBoost on seven buildings; calibration did not alter the CDF.

## J132_COFACTOR_TEST_interval_coverage — Test interval coverage and calibration
No distribution-free guarantee across new buildings with five calibration clusters.

## J133_COFACTOR_TEST_RMSE — Frozen test point prediction error
Tree point predictions and probabilistic predictive means; 64 MC draws for distributions.

## J134_COFACTOR_TEST_primary_building_delta — Primary CRPS difference across test buildings
Negative bars favour NGBoost; uncertainty across 7 same-city buildings is substantial.

## J135_COFACTOR_TEST_building_heterogeneity — Test building heterogeneity
Actual heterogeneity across the seven unseen Drammen buildings.

## J136_COFACTOR_TEST_tail_risk — Test extreme prediction audit
No post-hoc clipping or outlier exclusion; prior log-space clipping [0,30] fixed by P20.

## J137_COFACTOR_P22_validation_test_rank_reversal — Post-hoc validation-to-test probabilistic ranking reversal
Preselected direct seed 20262013 versus NGBoost Normal (40k FIT cap); cohorts differ and test may not be reused for tuning.

## J138_COFACTOR_P22_building_effect_uncertainty — Post-hoc seven-building paired contrast and uncertainty
Seven same-city building clusters; percentile bootstrap CI crosses zero and does not establish global superiority.

## J13_exploratory_interval_coverage — Interval coverage comparison
Observed coverage of nominal 90% intervals on an exploratory subset of the previously used validation data. Not independent publication evidence.

## J14_exploratory_interval_score — Interval score comparison
Mean central 90% interval score for conformal CatBoost, CQR and standard CFM variants. All on a reused validation partition.

## J15_exploratory_interval_width_distributions — Interval width distributions
Cumulative distributions of interval widths for three predictive methods on previously reused validation samples.

## J16_residual_cfm_actual_vs_predicted — Residual CFM — Actual vs Predicted
Observed and predicted annual total site energy for 900 exploratory validation samples.

## J17_exploratory_point_error_comparison — Point Prediction RMSE Comparison
Comparison of model RMSE on the same exploratory validation subset.

## J18_exploratory_residual_cfm_coverage — Prediction Interval Coverage
Empirical coverage of nominal 90% prediction intervals on reused validation data.

## J19_random_holdout_residual_prediction — Random-holdout residual CFM predictions
Observed versus predicted annual total site energy on original random test split (n=1,800).

## J20_random_holdout_rmse_comparison — Random-holdout model RMSE comparison
Point prediction RMSE for three frozen models on the same 1,800 random-holdout buildings.

## J21_random_holdout_coverage_width — Random-holdout interval efficiency
Observed 90% interval coverage versus average width for frozen probabilistic methods.

## J22_geometry_shift_feature_split — Prespecified geometry shift
Covariate-only distribution and cutoff for the frozen internal geometry-shift protocol.

## J23_geometry_shift_cohort_map — Geometry shift cohort map
Building length and height, with cohort membership determined without accessing target values.

## J24_geometry_shift_cfm_training_loss — Geometry-shift CFM training curves
Flow-matching validation loss by epoch for new training-split Standard and Residual CFM models; their target definitions differ, so numerical losses are not directly comparable.

## J25_geometry_shift_oof_residual_distribution — Out-of-fold residual distribution
Training-fit out-of-fold CatBoost prediction residual distribution; no OOD labels used.

## J26_height_ood_actual_vs_predicted — Height-OOD actual versus predicted
Matched observations and point predictions for frozen CatBoost and Residual CFM on the Height-OOD test.

## J27_height_ood_rmse_comparison — Height-OOD RMSE comparison
Point-prediction RMSE for three models retrained from scratch on the frozen geometry-shift split.

## J28_height_ood_interval_coverage — Height-OOD empirical coverage
Observed coverage before and after frozen in-domain calibration; no distribution-free coverage claim under shift.

## J29_height_ood_interval_width — Height-OOD prediction interval width
Mean widths of nominal 90% intervals for matched Height-OOD buildings.

## J30_height_ood_interval_score — Height-OOD interval score
Proper 90% interval score penalizing excessive width and missed target values.

## J31_height_ood_error_by_height — RMSE by OOD building height
RMSE by covariate-defined height group in the previously evaluated OOD cohort; descriptive only.

## J32_height_ood_coverage_by_height — 90% interval coverage by OOD building height
Empirical coverage of frozen calibrated 90% prediction intervals by height group; no shift-coverage guarantee.

## J33_height_ood_signed_bias_by_height — Signed prediction error by OOD height
Mean predicted minus observed annual total site energy by OOD height group; descriptive only.

## J34_indomain_multiseed_rmse — In-domain multi-seed RMSE
Validation-set RMSE for nine independently initialized CFM runs; CatBoost and OOF folds fixed.

## J35_indomain_ablation_rmse — In-domain model ablation (mean ± SD)
Comparison of Standard CFM, full OOF Residual CFM and a residual-flow ablation without CatBoost prediction in the condition.

## J36_indomain_paired_ablation — Paired-seed ablation differences
Paired differences in in-domain validation RMSE; negatives favor the full OOF residual CFM. Not a fresh holdout test.

## J37_indomain_multiseed_training_loss — Multi-seed training loss curves
Flow-loss trajectories for three variants. Loss magnitudes across standard and residual target definitions are not directly comparable.

## J38_indomain_uncalibrated_coverage — In-domain uncalibrated interval coverage
Empirical coverage of raw sample-quantile intervals by training seed. No conformal calibration or independent-test guarantee.

## J39_indomain_multiseed_crps — In-domain multi-seed CRPS
Empirical finite-sample CRPS for 64 generated energy samples per building; exploratory reused in-domain validation data.

## J40_seed_paired_conditioning_ablation — Paired-seed conditioning ablation
Fixed in-domain validation RMSE by paired CFM training seed; CatBoost and OOF folds held constant.

## J41_seed_paired_uncertainty_intervals — Seed-paired exploratory RMSE differences
95% t-intervals summarize CFM initialization variation on one reused validation set, not independent buildings or domains.

## J42_validation_energy_range_error_diagnostic — Validation energy-range error diagnostics
Observed annual-energy quintiles with CatBoost and prespecified first training seed 20262001; exploratory post-hoc comparison.

## J43_external_edcs_source_counts — EDCS independent source composition
Number of available EDCS records by courtyard shape, inferred from source filenames or sheet names; no energy labels accessed.

## J44_external_edcs_geometry_profile — EDCS source geometry feature distributions
Feature-only distributions of width, length, and height in the candidate independent-source EDCS dataset. Values are not energy outcomes.

## J45_edcs_external_validation_multiseed_rmse — EDCS L/O multi-seed RMSE
Exploratory L/O courtyard prediction, five CFM training seeds. Source-reported TOTAL_LOAD has conflicting published units.

## J46_edcs_external_source_ablation — EDCS model ablation (L/O validation)
Mean ± SD across five CFM training seeds; CatBoost is fitted once on the source dataset. U-shape holdout not evaluated.

## J47_edcs_external_uncalibrated_coverage — EDCS raw 90% interval coverage
Uncalibrated sample quantile intervals on reused L/O validation; not calibrated or U-shape independent coverage.

## J48_edcs_external_observed_vs_predicted — EDCS observed versus predicted (L/O validation)
EDCS native Total_Load values; original publication does not consistently describe units or time aggregation.

## J49_edcs_U_frozen_rmse — Frozen EDCS U-shape RMSE
RMSE on the U-shaped courtyard holdout after prespecified L/O calibration; five-seed CFM mixture versus CatBoost.

## J50_edcs_U_coverage — Frozen U-shape interval coverage
Raw predictive intervals exist for CFM only; CatBoost has only an L/O conformal interval. No under-shift coverage guarantee.

## J51_edcs_U_primary_bootstrap — EDCS U-holdout primary RMSE contrast
Paired row bootstrap of 2,000 replicates; simulation row correlation may make intervals optimistic.

## J52_edcs_U_observed_predicted — EDCS U-shape observed vs predicted
Frozen U-shaped holdout observed and predicted Total_Load with source unit ambiguity retained.

## J53_edcs_U_calibrated_interval_score — EDCS U-shape interval score
Interval score penalizes overly wide intervals and prediction interval misses. Lower is better.

## J54_edcs_U_absolute_error — EDCS U-shape absolute error distribution
Median and interquartile spread of absolute prediction error on the frozen U-shape holdout.

## J55_edcs_calibration_to_U_coverage_shift — Frozen EDCS coverage shift
Observed 90% interval coverage on L/O calibration and independently evaluated U shape, no post-test adjustment.

## J56_edcs_U_width_coverage_tradeoff — EDCS U sharpness-reliability trade-off
The nominal 90% interval may be too narrow under shape shift; wide CatBoost interval can attain conservative coverage.

## J57_edcs_validation_U_ranking_reversal — EDCS validation-to-U method ranking reversal
Relative performance versus CatBoost within each cohort. L/O values are five single-seed RMSE means, U values are five-seed mixture RMSEs; differences are not controlled effects of shape alone.

## J58_edcs_U_prediction_strata_RMSE — EDCS U RMSE by pre-existing point forecast quartile
Post-hoc U diagnostic. Quartiles were derived from frozen CatBoost predictions rather than observed target levels.

## J59_edcs_U_seedwise_RMSE_diagnostic — EDCS U single-seed stability diagnostic
Five training seeds per variant, all frozen before first U target access. These are post-hoc measurements, not a reason to choose a seed on U.

## J60_five_climate_source_city_counts — Independent source city counts
Scenario counts by reported city in the new official supplementary CSV; labels and annual cooling outcomes were not read.

## J61_five_climate_frozen_feature_only_split — Independent-source feature-only split
Fit, validation and calibration partitions are grouped by identical architecture designs. Miami is a held-out climate within the same simulation source.

## J62_fiveclimate_source_native_target_distribution — Five-climate training target distribution
FIT and Validation target distribution only; publisher column and article unit descriptions are not assumed interchangeable.

## J63_fiveclimate_multiseed_validation_rmse — Five-climate multi-seed validation RMSE
Five CFM seeds compared with separately frozen CatBoost and published-method RandomForest baselines.

## J64_fiveclimate_architecture_ablation — Independent-source method ablation
Mean and standard deviation across five CFM training seeds; exploratory validation evidence only.

## J65_fiveclimate_uncalibrated_validation_coverage — Five-climate raw interval coverage
Uncalibrated prediction interval coverage on validation. Miami/calibration labels not inspected.

## J66_fiveclimate_validation_observed_vs_predicted — Five-climate observed versus predicted
Frozen CatBoost and one predeclared training seed, in-source validation only.

## J67_fiveclimate_validation_citywise_rmse — Four-climate validation citywise RMSE
Citywise validation RMSE. CFM values averaged across five seeds; Miami excluded.

## J68_fiveclimate_Miami_frozen_RMSE — Frozen Miami RMSE
Frozen models evaluated on the Miami climate holdout; comparison uses source-native numeric target.

## J69_fiveclimate_Miami_raw_vs_frozen_calibrated_coverage — Miami calibrated coverage
Nominal 90% interval coverage on the Miami holdout before/after nonnegative expansion locked in four-climate calibration.

## J70_fiveclimate_calibration_to_Miami_coverage_shift — Four-climate calibration versus Miami coverage
Coverage of the same frozen interval rules on four-climate calibration and unseen Miami simulation conditions.

## J71_fiveclimate_Miami_frozen_primary_scatter — Frozen Miami primary scatter
CatBoost versus five-seed no-base residual CFM on the same frozen Miami cohort.

## J72_fiveclimate_Miami_primary_cluster_bootstrap — Miami primary cluster-bootstrap uncertainty
Paired architecture-design cluster bootstrap of primary fixed-method RMSE difference; descriptive, not proof of population inference.

## J73_fiveclimate_Miami_width_coverage_tradeoff — Miami width-coverage trade-off
Prediction interval coverage and average width after calibration frozen on the four non-Miami climates.

## J74_Miami_frozen_target_distribution_shift — Frozen Miami target distribution shift
Observed objective distribution of four-climate fit and validation versus previously frozen Miami holdout.

## J75_Miami_frozen_allmodel_observed_predicted — All frozen Miami model predictions
Actual-versus-predicted scatter for each predeclared method on the already evaluated Miami holdout.

## J76_Miami_frozen_signed_prediction_bias — Frozen Miami model signed prediction bias
Signed mean bias with previously frozen predictions; negative bias indicates systematic underprediction.

## J77_Miami_frozen_feature_shift_and_OOV — Frozen encoded-feature and unknown-category audit
Comparison of frozen fit-only encoded feature distribution with Miami; city Miami is outside the fit vocabulary.

## J78_Miami_frozen_interval_failure_direction — Frozen Miami prediction interval failures
Percentage of Miami outcomes below, inside and above the frozen 90% prediction intervals.

## J79_frozen_Miami_design_matched_target_comparison — Same-design source-to-Miami observed energy contrast
Descriptive paired building-design comparison; Miami labels were already inspected and physical climate covariates were not modeled.

## J80_frozen_Miami_RMSE_by_design_familiarity — Frozen Miami RMSE by design familiarity
Post-hoc error strata for all prespecified models; same design in FIT does not imply Miami climate was observed.

## J81_frozen_Miami_matched_design_target_shift — Miami design-matched target displacement
Distribution of Miami-minus-four-climate-FIT observed target differences for architectures shared across cities; descriptive, noncausal.

## J82_BDG2_measured_source_site_inventory — BDG2 available electricity meter buildings by site
Number of buildings with an electricity meter header matched to building metadata per eligible site; no meter readings accessed.

## J83_BDG2_measured_frozen_site_roles — BDG2 source-site role assignments
Feature-only site partition assignments before meter readings, weather series or target values are inspected.

## J84_BDG2_meter_weather_timestamp_alignment — BDG2 source-local weather vs meter timestamps
Percentage of hourly meter timestamps matched by weather timestamps by site. Timestamp comparisons do not use energy outcomes.

## J85_BDG2_fit_only_meter_quality — BDG2 fit-only electricity meter coverage
Number of electricity meter columns passing predeclared training-site availability and nonnegative-reading checks. No validation/calibration/test meter data read.

## J86_BDG2_weather_feature_missingness — BDG2 site-weather feature missingness
Feature-only weather data completeness for site-registered meteorological attributes; no energy target values from held-out sites.

## J87_BDG2_validation_hourly_electricity_distribution — BDG2 measured hourly electricity distribution
Source-measured hourly electricity consumption in two validation sites (raw numeric kWh transformed only for axis).

## J88_BDG2_multiseed_validation_RMSE — BDG2 site-heldout five-seed RMSE
Mean and standard deviation over five CFM initialization seeds, measured electricity hourly kWh.

## J89_BDG2_multiseed_validation_coverage — BDG2 raw interval coverage
Uncalibrated measured electricity hourly prediction interval coverage; not a calibration guarantee.

## J90_BDG2_validation_actual_vs_predicted — BDG2 actual vs predicted hourly electricity
Exploratory validation: CatBoost and one prespecified no-base residual seed, plot clipped to 99th observed percentile for visibility.

## J91_BDG2_validation_sitewise_RMSE — BDG2 sitewise validation RMSE
Separate error for each of two heldout validation sites; site clusters are the appropriate uncertainty unit.

## J92_BDG2_validation_seedwise_extreme_RMSE — BDG2 seedwise RMSE / log scale
Seedwise validation RMSE on two frozen unseen sites; log scale shows rare catastrophic outcomes.

## J93_BDG2_validation_top1pct_SSE_share — BDG2 worst 1% SSE concentration
Proportion of total squared error contributed by the top 1% largest absolute-error rows; no clipping applied.

## J94_BDG2_validation_maximum_prediction_by_seed — BDG2 maximum predictive mean by seed
Maximum of saved frozen point predictions, revealing whether rare inverse-log excursions dominate errors.

## J95_BDG2_validation_two_site_seedwise_RMSE — BDG2 validation sitewise RMSE variation
Separate sitewise RMSE per CFM seed and variant versus CatBoost; only two validation sites, descriptive only.

## J96_BDG2_validation_absolute_error_ECDF — BDG2 frozen validation absolute-error ECDF
Exploratory error magnitude distributions for CatBoost and the first fixed no-base/standard CFM seed; curves truncated for visual clarity only.

## J97_BDG2_three_site_test_RMSE — BDG2 three-site frozen model comparison
RMSE for fixed baselines and five-seed CFM mixtures, three independent heldout BDG2 sites.

## J98_BDG2_three_site_test_coverage — BDG2 independent-site interval coverage
Empirical 90% interval coverage after frozen separate-site calibration, without marginal coverage guarantee.

## J99_BDG2_three_site_RMSE_by_site — BDG2 sitewise RMSE
Independent three-site differences in measured hourly electricity estimation error; each site is a cluster.
