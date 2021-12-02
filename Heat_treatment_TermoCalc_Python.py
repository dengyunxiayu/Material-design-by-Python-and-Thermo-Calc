
from tc_python import *
import matplotlib.pyplot as plt
#import numpy as np

#in this example I create a temperature profile knowing the cooling time which is not your case.
#some variables for which I know the value
f2 = open('Design_par.txt', "r")
lines=list(f2.readlines())
temp_2 = float(lines[0].strip('\n'))
time_holding1=float(lines[1].strip('\n'))
dT_dt_cooling = 5 #cooling rate
temp_3 = float(lines[2].strip('\n'))
time_holding2 = float(lines[3].strip('\n'))
dT_dt_heating = 10  # cooling rate
# time_holding = 15
f2.close()
#what is the temperature after colling for 10 sec at 5 degrees per second
time_cooling = (1523 - temp_2) / dT_dt_cooling
#what is the time after both a cooling of 10 sec and holding for 50 sec
time_3 = time_cooling + time_holding1

#Now I have all the data

f3=open('holding1.txt',"w")
f3.write('{} {} {} {}'.format(0., ' ', 1523, '\n'))     #the {} is to tell the code you will have to write 4 items including the values, the space (' '), and the line break ('\n')
f3.write('{} {} {} {}'.format(time_cooling, ' ', temp_2, '\n'))
f3.write('{} {} {} {}'.format(time_3, ' ', temp_2, '\n'))
f3.close()
# what is the temperature after colling for 10 sec at 5 degrees per second
time_heating = (temp_3 - 300) / dT_dt_heating
# what is the time after both a cooling of 10 sec and holding for 50 sec
time_6 = time_heating + time_holding2
# Now I have all the data

f5 = open('holding2.txt', "w")
f5.write('{} {} {} {}'.format(0., ' ', 801, '\n'))  # the {} is to tell the code you will have to write 4 items including the values, the space (' '), and the line break ('\n')
f5.write('{} {} {} {}'.format(time_heating, ' ', temp_3, '\n'))
f5.write('{} {} {} {}'.format(time_6, ' ', temp_3, '\n'))
f5.write('{} {}'.format('1e-3', '\n'))
f5.write('{} {}'.format('1e-3', '\n'))
f5.write('{} {}'.format('1e-3', '\n'))
f5.write('{} {}'.format('1e-3', '\n'))
f5.write('{} {}'.format("MartensitePct", '\n'))
f5.write('{} {}'.format("fv_init", '\n'))
f5.write('{} {}'.format("r_pinit", '\n'))
f5.close()

#in the precipitation code
with TCPython():
    #vectors that are defined here for the values of the time and temperature
    time_prof = {}
    temp_prof={}

    Profile = TemperatureProfile()    #I tell the code that I would like to create an object TemperatureProfile() that I call Profile
    #we need now to fill this object
    f3=open('holding1.txt',"r")  #I open the file previously generated

    for i in range(0,3):
        time_prof[i], temp_prof[i] = [float(s) for s in f3.readline().split()] #for the program, the text file is just a chain of characters, a long string - I tell the program to convert the characters chains in floats and that they are spearated by empty characters (split)
        Profile.add_time_temperature(time_prof[i], temp_prof[i]) #I add in the object nammed Profile that is a TemperatureProfile type the lines
        #simulation_time=time_prof[0]+time_prof[1]+time_prof[2]
    print(time_prof[2])
    print('ok')

    #exit()

    sim_results = (SetUp().set_cache_folder(os.path.basename(__file__) + "_cache1")
                   .select_thermodynamic_and_kinetic_databases_with_elements("TCFE8", "MOBFE4", ["Fe", "C", "Si", "Mn", "Cr", "S", "P"])
                   .get_system()
                   .with_non_isothermal_precipitation_calculation()
                   .set_composition_unit(CompositionUnit.MASS_PERCENT)
                   .set_composition("C", 0.68)
                   .set_composition("Si", 0.4)
                   .set_composition("Mn", 0.7)
                   .set_composition("Cr", 13)
                   .set_composition("S", 0.025)
                   .set_composition("P", 0.01)
                   .with_matrix_phase(MatrixPhase("FCC_A1")
                        .add_precipitate_phase(PrecipitatePhase("M7C3")))
                   .with_temperature_profile(Profile)
                   .set_simulation_time(time_prof[2])
                   .calculate()
                   )

    fv_init_M7C3_1 = sim_results.get_volume_fraction_of('M7C3')[1]
    r_pinit_M7C3_1 = sim_results.get_mean_radius_of('M7C3')[1]
    N_Dinit_M7C3_1 = sim_results.get_number_density_of('M7C3')[1]
    M7C3_C = sim_results.get_precipitate_composition_in_mole_fraction_of('M7C3','C')[1][-1]
    M7C3_Si = sim_results.get_precipitate_composition_in_mole_fraction_of('M7C3', 'Si')[1][-1]
    M7C3_Mn = sim_results.get_precipitate_composition_in_mole_fraction_of('M7C3', 'Mn')[1][-1]
    M7C3_Cr = sim_results.get_precipitate_composition_in_mole_fraction_of('M7C3', 'Cr')[1][-1]
    M7C3_S = sim_results.get_precipitate_composition_in_mole_fraction_of('M7C3', 'S')[1][-1]
    M7C3_P = sim_results.get_precipitate_composition_in_mole_fraction_of('M7C3', 'P')[1][-1]
    N_D_Distri_r_M7C3 = sim_results.get_number_density_distribution_for_radius_of('M7C3',time_prof[2])
    Size_Distri_r_M7C3 = sim_results.get_size_distribution_for_radius_of('M7C3',time_prof[2])
    XC_mat = sim_results.get_matrix_composition_in_mole_fraction_of('C')[1][-1]
    XSi_mat = sim_results.get_matrix_composition_in_mole_fraction_of('Si')[1][-1]
    XMn_mat = sim_results.get_matrix_composition_in_mole_fraction_of('Mn')[1][-1]
    XCr_mat = sim_results.get_matrix_composition_in_mole_fraction_of('Cr')[1][-1]
    XS_mat = sim_results.get_matrix_composition_in_mole_fraction_of('S')[1][-1]
    XP_mat = sim_results.get_matrix_composition_in_mole_fraction_of('P')[1][-1]
    print(fv_init_M7C3_1[-1])
    print(r_pinit_M7C3_1[-1])
    print(N_Dinit_M7C3_1[-1])
    print(M7C3_C)
    print(M7C3_Si)
    print( M7C3_Mn)
    print(M7C3_Cr)
    print(M7C3_S)
    print(M7C3_P)
    #print(N_D_Distri_r_M7C3)
    #print(Size_Distri_r_M7C3)
    print(XC_mat)
    print(XSi_mat)
    print(XMn_mat)
    print(XCr_mat)
    print(XS_mat)
    print(XP_mat)
    for j in range(0, len(N_D_Distri_r_M7C3[1])):
        print(N_D_Distri_r_M7C3[0][j], N_D_Distri_r_M7C3[1][j])
    #for j in range(0, 213):
        #print(Size_Distri_r_M7C3[0][j], Size_Distri_r_M7C3[1][j])
    #exit()

    result_3 = (SetUp().select_database_and_elements("TCFE9", ["Fe", "C", "Cr", "Si", "Mn", "S", "P"])
                .get_system()
                .with_property_model_calculation("Martensite Fractions")
                .set_composition_unit(CompositionUnit.MOLE_FRACTION)
                .set_composition("C", XC_mat)
                .set_composition("Si", XSi_mat)
                .set_composition("Mn", XMn_mat)
                .set_composition("Cr",XCr_mat)
                .set_composition("S", XS_mat)
                .set_composition("P", XP_mat)
                .set_temperature(300)#room temperature
                .calculate()
                )
    print("Available result quantities: {}".format(result_3.get_result_quantities()))
    print("Available result quantities: {}".format(result_3.get_value_of("MartensitePct")))
    MartensitePct = result_3.get_value_of("MartensitePct")
    print('MartensitePct',MartensitePct)
    #exit()
    # Storage of the precipitate distribution of M7C3
    for i in range(0, len(N_D_Distri_r_M7C3[1])):
        f7 = open('Size_profile.txt', "w")
        for j in range(0, len(N_D_Distri_r_M7C3[1])):
            f7.write('{} {} {} {}'.format(N_D_Distri_r_M7C3[0][j], ' ', N_D_Distri_r_M7C3[1][j], '\n'))
        f7.close()
    radius = {}
    N_D = {}
    Size_profile = ParticleSizeDistribution()
    Size_profile.set_volume_fraction_of_phase_type(VolumeFractionOfPhaseType.VOLUME_PERCENT)
    Size_profile.set_volume_fraction_of_phase_value(fv_init_M7C3_1[-1] * 100)  # to use this object, we should specify the volume fraction of M7C#
    Size_profile.set_initial_composition('C', M7C3_C)
    Size_profile.set_initial_composition('Si', M7C3_Si)  # precipitates do not contain Si
    Size_profile.set_initial_composition('Mn', M7C3_Mn)
    Size_profile.set_initial_composition('Cr', M7C3_Cr)
    Size_profile.set_initial_composition('S', M7C3_S)
    Size_profile.set_initial_composition('P', M7C3_P)
    f8 = open('Size_profile.txt', "r")
    for i in range(0, len(N_D_Distri_r_M7C3[1])):
        radius[i], N_D[i] = [float(s) for s in f8.readline().split()]  # for the program, the text file is just a chain of characters, a long string - I tell the program to convert the characters chains in floats and that they are spearated by empty characters (split)
        print(radius[i], N_D[i])
        Size_profile.add_radius_and_number_density(radius[i], N_D[i])
        #Size_profile.

    #exit()

    time_prof2 = {}
    temp_prof2 = {}

    Profile2 = TemperatureProfile()  # I tell the code that I would like to create an object TemperatureProfile() that I call Profile
    f6 = open('holding2.txt', "r")  # I open the file previously generated

    for k in range(0, 3):
        time_prof2[k], temp_prof2[k] = [float(s) for s in f6.readline().split()]  # for the program, the text file is just a chain of characters, a long string - I tell the program to convert the characters chains in floats and that they are spearated by empty characters (split)
        Profile2.add_time_temperature(time_prof2[k], temp_prof2[k])  # I add in the object nammed Profile that is a TemperatureProfile type the lines
    print(time_prof2[2])
    print('ok')

    sim_results_2 = (SetUp().set_cache_folder(os.path.basename(__file__) + "_cache2")
                     .select_thermodynamic_and_kinetic_databases_with_elements("TCFE9", "MOBFE4", ["Fe", "C", "Si", "Mn", "Cr","S","P"])
                     .get_system()
                     .with_isothermal_precipitation_calculation()
                     .set_composition_unit(CompositionUnit.MASS_PERCENT)
                     .set_composition("C", 0.68)
                     .set_composition("Si", 0.4)
                     .set_composition("Mn", 0.7)
                     .set_composition("Cr", 13)
                     .set_composition("S", 0.025)
                     .set_composition("P", 0.01)
                     #.with_temperature_profile(Profile2)
                     .set_simulation_time(time_holding2)
                     .set_temperature(temp_prof2[2])
                     .with_matrix_phase(MatrixPhase("BCC_A2")
                        .add_precipitate_phase(PrecipitatePhase('M7C3')
                             .with_particle_size_distribution(Size_profile))
                        .add_precipitate_phase(PrecipitatePhase('M23C6')))
                     .calculate()
                     )
    #exit()

    fvM7 = sim_results_2.get_volume_fraction_of('M7C3')[1][-1]
    print('test :', fvM7)
    fvM23 = sim_results_2.get_volume_fraction_of('M23C6')[1][0]
    print('test :', fvM23)
    fv_init_M7C3_2 = sim_results_2.get_volume_fraction_of('M7C3')[1]
    r_pinit_M7C3_2 = sim_results_2.get_mean_radius_of('M7C3')[1]
    N_Dinit_M7C3_2 = sim_results_2.get_number_density_of('M7C3')[1]
    M7C3_C_2 = sim_results_2.get_precipitate_composition_in_mole_fraction_of('M7C3', 'C')[1]
    M7C3_Si_2 = sim_results_2.get_precipitate_composition_in_mole_fraction_of('M7C3', 'Si')[1]
    M7C3_Mn_2 = sim_results_2.get_precipitate_composition_in_mole_fraction_of('M7C3', 'Mn')[1]
    M7C3_Cr_2 = sim_results_2.get_precipitate_composition_in_mole_fraction_of('M7C3', 'Cr')[1]
    M7C3_S_2 = sim_results_2.get_precipitate_composition_in_mole_fraction_of('M7C3', 'S')[1]
    M7C3_P_2 = sim_results_2.get_precipitate_composition_in_mole_fraction_of('M7C3', 'P')[1]
    fv_init_M23C6_2 = sim_results_2.get_volume_fraction_of('M23C6')[1]
    r_pinit_M23C6_2 = sim_results_2.get_mean_radius_of('M23C6')[1]
    N_Dinit_M23C6_2 = sim_results_2.get_number_density_of('M23C6')[1]
    M23C6_C_2 = sim_results_2.get_precipitate_composition_in_mole_fraction_of('M23C6', 'C')[1]
    M23C6_Si_2 = sim_results_2.get_precipitate_composition_in_mole_fraction_of('M23C6', 'Si')[1]
    M23C6_Mn_2 = sim_results_2.get_precipitate_composition_in_mole_fraction_of('M23C6', 'Mn')[1]
    M23C6_Cr_2 = sim_results_2.get_precipitate_composition_in_mole_fraction_of('M23C6', 'Cr')[1]
    M23C6_S_2 = sim_results_2.get_precipitate_composition_in_mole_fraction_of('M23C6', 'S')[1]
    M23C6_P_2 = sim_results_2.get_precipitate_composition_in_mole_fraction_of('M23C6', 'P')[1]
    XC_mat_2 = sim_results_2.get_matrix_composition_in_mole_fraction_of('C')[1]
    XSi_mat_2 = sim_results_2.get_matrix_composition_in_mole_fraction_of('Si')[1]
    XMn_mat_2 = sim_results_2.get_matrix_composition_in_mole_fraction_of('Mn')[1]
    XCr_mat_2 = sim_results_2.get_matrix_composition_in_mole_fraction_of('Cr')[1]
    XS_mat_2 = sim_results_2.get_matrix_composition_in_mole_fraction_of('S')[1]
    XP_mat_2 = sim_results_2.get_matrix_composition_in_mole_fraction_of('P')[1]
    print('After second holding')
    print('Mean sizes M23C6: ', r_pinit_M23C6_2[-1], 'M7C3 : ', r_pinit_M7C3_2[-1])
    print('Volume fractions M23C6: ', fv_init_M23C6_2[-1], 'M7C3 : ', fv_init_M7C3_2[-1])
    print('Number Density M23C6: ', N_Dinit_M23C6_2[-1], 'M7C3 : ', N_Dinit_M7C3_2[-1])
    print('Initial volume fraction: ', sim_results_2.get_volume_fraction_of('M7C3')[1][0])
    print('Initial radius : ', sim_results_2.get_mean_radius_of('M7C3')[1][0])
    print('Initial number density: ', sim_results_2.get_number_density_of('M7C3')[1][0])
    print('Composition of M23C6:', 'C:', M23C6_C_2[-1], 'Si:', M23C6_Si_2[-1], 'Mn:', M23C6_Mn_2[-1], 'Cr:', M23C6_Cr_2[-1], 'S:',M23C6_S_2[-1], 'P:',M23C6_P_2[-1]  )
    print('Composition of M7C3:', 'C:', M7C3_C_2[-1], 'Si:', M7C3_Si_2[-1], 'Mn:', M7C3_Mn_2[-1], 'Cr:', M7C3_Cr_2[-1], 'S:', M7C3_S_2[-1], 'P:', M7C3_P_2[-1])
    print('Composition of Matrix:', 'C:', XC_mat_2[-1], 'Si:', XSi_mat_2[-1], 'Mn:', XMn_mat_2[-1], 'Cr:',XCr_mat_2[-1], 'S:', XS_mat_2[-1], 'P:',XP_mat_2[-1])

    f5 = open('Holding2.txt', "w")
    # f5.write('{} {} {} {}'.format(0., ' ', 500, '\n'))  # the {} is to tell the code you will have to write 4 items including the values, the space (' '), and the line break ('\n')
    # f5.write('{} {} {} {}'.format(time_heating, ' ', temp_3, '\n'))
    # f5.write('{} {} {} {}'.format(time_6, ' ', temp_3, '\n'))
    f5.write('{} {}'.format(fv_init_M23C6_2[-1], '\n'))
    f5.write('{} {}'.format(fv_init_M7C3_2[-1], '\n'))
    f5.write('{} {}'.format(r_pinit_M23C6_2[-1], '\n'))
    f5.write('{} {}'.format(r_pinit_M7C3_2[-1], '\n'))
    f5.write('{} {}'.format(MartensitePct, '\n'))
    f5.close()
    # exit()

f9 = open('Design_par.txt', "w")
f9.write('{} {}'.format(temp_2, '\n'))
f9.write('{} {}'.format(time_holding1, '\n'))
f9.write('{} {}'.format(temp_3, '\n'))
f9.write('{} {}'.format(time_holding2, '\n'))
f9.close()

f10 = open('fv_rp_martensite.txt', "w")
f10.write('{} {}'.format(fv_init_M23C6_2[-1], '\n'))
f10.write('{} {}'.format(fv_init_M7C3_2[-1], '\n'))
f10.write('{} {}'.format(r_pinit_M23C6_2[-1], '\n'))
f10.write('{} {}'.format(r_pinit_M7C3_2[-1], '\n'))
f10.write('{} {}'.format(MartensitePct, '\n'))
f10.close()

# Plots

# fig1, ax = plt.subplots()
# fig1.suptitle('Carbides precipitation', fontsize=14, fontweight='bold')
# ax.set_xlabel('Time [s]')
# ax.set_ylabel('Volume Fraction')
# ax.semilogx(fv_init_M7C3_1, 'r-', label="Volume fraction of M7C3")
# ax.legend()
# plt.show()

# fig2, ax = plt.subplots()
# fig2.suptitle('Carbides precipitation', fontsize=14, fontweight='bold')
# ax.set_xlabel('Time [s]')
# ax.set_ylabel('Number Density')
# ax.semilogx(N_Dinit_M7C3_1, 'r-', label="Number Density of M7C3")
# ax.legend()
# plt.show()

# Plot result
# fig3, ax = plt.subplots()
# fig3.suptitle('Carbides precipitation', fontsize=14, fontweight='bold')
# ax.set_xlabel('Time [s]')
# ax.set_ylabel('Volume Fraction')
# ax.semilogx(fv_init_M7C3_2, 'r-', label="Volume fraction of M7C3")
# ax.semilogx(fv_init_M23C6_2, 'g-', label="Volume fraction of M23C6")
# ax.legend()
# plt.show()

# fig4, ax = plt.subplots()
# fig4.suptitle('Carbides precipitation', fontsize=14, fontweight='bold')
# ax.set_xlabel('Time [s]')
# ax.set_ylabel('Number Density')
# ax.semilogx(N_Dinit_M7C3_2, 'r-', label="Number Density of M7C3")
# ax.semilogx(N_Dinit_M23C6_2, 'g-', label="Number Density of M23C6")
# ax.legend()
# plt.show()
