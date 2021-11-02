# Requirement: python3
import math

# Constant
c = 3e8  # light velocity, m/s unit
D_Hertzian = 1.5  # directivity of Hertzian dipole
D_halfwave = 1.64  # directivity of halfwave dipole
mu = 4 * math.pi * 1e-7  # Magnetic permeability of cooper (=vacuum), H/m unit
sigma = 5.8 * 1e7  # electrical conductivity of copper, S/m unit
Rrad_halfwave = 73  # radiation resistance of halfwave dipole, Ohm unit

print('**** Please input parameters in SI units ****\n')

# Input section
print('---INPUT SECTION---')
I = float(input('Current amplitude I (in Ampere): I = '))
f = float(input('Frequency (in Hertz): '))
R = float(input('Distance R between 2 antennas (in meter): R = '))
a1 = float(input('Radius a1 of transmitting antenna (in meter): a1 = '))
l1 = float(input('Length l1 of transmitting antenna (in meter): l1 = '))
a2 = float(input('Radius a2 of receiving antenna (in meter): a2 = '))
l2 = float(input('Length l2 of receiving antenna (in meter): l2 = '))

# Helper function section
lamda = c / f


def Smax_Hertzian(l):  # maximum power density of Hertzian dipole
    return 15 * math.pi * (I**2) * (l**2) / (R**2 * lamda**2)


def Prad_Hertzian(l):  # total radiated power of Hertzian dipole
    return 40 * (math.pi**2) * (I**2) * (l**2) / (lamda**2)


def Rloss(l, a):  # Rloss of the antenna
    return (l / (2 * math.pi * a)) * math.sqrt(math.pi * mu * f / sigma)


def Rrad_Hertzian(l):  # Rrad of Hertzian dipole
    return 80 * (math.pi**2) * (l/lamda)**2


def Smax_halfwave(l):  # maximum power density of half-wave dipole
    return 15 * (I**2) / (math.pi * R**2)


def Prad_halfwave():  # total radiated power of half-wave dipole
    return 36.6 * (I**2)


def efficiency(Rrad, Rloss):  # radiation efficiency
    return Rrad / (Rrad + Rloss)


def gain(e, D):  # antenna gain
    return e * D


def eff_area(D):  # effective area
    return lamda**2 * D / (4 * math.pi)


def Ptrans(Rrad, Rloss):  # transmitting power
    return 1/2 * (I**2) * (Rrad + Rloss)


def Prec(Ptrans, G_trans, G_rec):  # receiving power
    return Ptrans * G_trans * G_rec * (lamda/(4*math.pi*R))**2


def Hertzian_trans():
    Smax = Smax_Hertzian(l1)
    Rloss_trans = Rloss(l1, a1)
    Rrad_trans = Rrad_Hertzian(l1)
    Prad = Prad_Hertzian(l1)
    Pt = Ptrans(Rrad_trans, Rloss_trans)
    eff_trans = efficiency(Rrad_trans, Rloss_trans)
    D_trans = D_Hertzian
    G_trans = gain(eff_trans, D_trans)
    return Smax, Rloss_trans, Rrad_trans, Prad, Pt, eff_trans, D_trans, G_trans


def Hertzian_rec():
    Rloss_rec = Rloss(l2, a2)
    Rrad_rec = Rrad_Hertzian(l2)
    eff_rec = efficiency(Rrad_rec, Rloss_rec)
    D_rec = D_Hertzian
    G_rec = gain(eff_rec, D_rec)
    return Rloss_rec, Rrad_rec, eff_rec, D_rec, G_rec


def Halfwave_trans():
    Smax = Smax_halfwave(l1)
    Rloss_trans = Rloss(l1, a1)
    Rrad_trans = Rrad_halfwave
    Prad = Prad_halfwave()
    Pt = Ptrans(Rrad_trans, Rloss_trans)
    eff_trans = efficiency(Rrad_trans, Rloss_trans)
    D_trans = D_halfwave
    G_trans = gain(eff_trans, D_trans)
    return Smax, Rloss_trans, Rrad_trans, Prad, Pt, eff_trans, D_trans, G_trans


def Halfwave_rec():
    Rloss_rec = Rloss(l2, a2)
    Rrad_rec = Rrad_halfwave
    eff_rec = efficiency(Rrad_rec, Rloss_rec)
    D_rec = D_halfwave
    G_rec = gain(eff_rec, D_rec)
    return Rloss_rec, Rrad_rec, eff_rec, D_rec, G_rec


def print_valid_antennas(Smax, Prad, eff_trans, D_trans, G_trans,
                        eff_rec, D_rec, G_rec, Pr):
    print('Maximum power density: ', Smax, '(W/m^2)')
    print('\n****Assume two antennas are oriented in the direction of maximum power.****')
    print('Radiation power: ', Prad, '(W)')
    print('Efficiency of transmitting antenna: ', eff_trans)
    print('Directivity of transmitting antenna: ', D_trans)
    print('Gain of transmitting antenna: ', G_trans)
    print('\nEfficiency of receiving antenna: ', eff_rec)
    print('Directivity of receiving antenna: ', D_rec)
    print('Gain of receiving antenna: ', G_rec)
    print('\nReceiving power: ', Pr, '(W)')


# Calculation section
print('---OUTPUT SECTION---')
if 0 < l1/lamda < 1/50 and 0 < l2/lamda < 1/50:
    # 2 antennas are Hertzian dipoles.
    Smax, Rloss_trans, Rrad_trans, Prad, Pt, eff_trans, D_trans, G_trans = Hertzian_trans()
    Rloss_rec, Rrad_rec, eff_rec, D_rec, G_rec = Hertzian_rec()
    Pr = Prec(Pt, G_trans, G_rec)
    print('Both antennas are Hertzian dipoles')
    print('Power density: ' + str(Smax) + ' * sin(theta)^2 (W/m^2)')
    print_valid_antennas(Smax, Prad, eff_trans, D_trans, G_trans,
                         eff_rec, D_rec, G_rec, Pr)

elif 0 < l1/lamda < 1/50 and abs(2*l2 - lamda) < 1e-4:
    # transmitting antenna is Hertzian dipole,
    # receiving antenna is half-wave length dipole.
    Smax, Rloss_trans, Rrad_trans, Prad, Pt, eff_trans, D_trans, G_trans = Hertzian_trans()
    Rloss_rec, Rrad_rec, eff_rec, D_rec, G_rec = Halfwave_rec()
    Pr = Prec(Pt, G_trans, G_rec)
    print('Transmitting antenna is a Hertzian dipoles. Receiving antenna is a half-wave length dipole.')
    print('Power density: ' + str(Smax) + ' * sin(theta)^2 (W/m^2)')
    print_valid_antennas(Smax, Prad, eff_trans, D_trans, G_trans,
                         eff_rec, D_rec, G_rec, Pr)

elif abs(2*l1 - lamda) < 1e-4 and 0 < l2/lamda < 1/50:
    # transmitting antenna is half-wave length dipole,
    # receiving antenna is Hertzian dipole.
    Smax, Rloss_trans, Rrad_trans, Prad, Pt, eff_trans, D_trans, G_trans = Halfwave_trans()
    Rloss_rec, Rrad_rec, eff_rec, D_rec, G_rec = Hertzian_rec()
    Pr = Prec(Pt, G_trans, G_rec)
    print('Transmitting antenna is half-wave length dipoles. Receiving antenna is a Hertzian dipole.')
    print('Power density: ' + str(Smax) + ' * cos[pi/2 * cos(theta)]^2 / sin(theta)^2 (W/m^2)')
    print_valid_antennas(Smax, Prad, eff_trans, D_trans, G_trans,
                         eff_rec, D_rec, G_rec, Pr)

elif abs(2*l1 - lamda) < 1e-4 and abs(2*l2 - lamda) < 1e-4:
    # 2 antennas are half-wave length dipoles.
    Smax, Rloss_trans, Rrad_trans, Prad, Pt, eff_trans, D_trans, G_trans = Halfwave_trans()
    Rloss_rec, Rrad_rec, eff_rec, D_rec, G_rec = Halfwave_rec()
    Pr = Prec(Pt, G_trans, G_rec)
    print('Both antenna are half-wave length dipoles.')
    print('Power density: ' + str(Smax) + ' * cos[pi/2 * cos(theta)]^2 / sin(theta)^2 (W/m^2)')
    print_valid_antennas(Smax, Prad, eff_trans, D_trans, G_trans,
                         eff_rec, D_rec, G_rec, Pr)

else:
    print('Please check the length of antennas as some requirements for Hertzian and Half-wave length antenna are not met.')








