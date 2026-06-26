# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 17:27:02 2019
@author: olivaren
"""


def maindeffun(name, matr, Divergence, numirr, wavelen):
    from mirrorRef2 import thickmirror2
    import numpy as np
    import pandas as pd
    import math

    # FIXED PARAMETERS:
    lambdamin = '2.0'
    lambdamax = '40.0'
    lambdanum = '100'
    density = -1
    roughness = '0.3'

    # VARIABLES (ASKED IN THE GUI):
    pol = 1

    # MATR, OBTAINED IN GUI: WE WILL SUPPOSE NO VLS GRATINGS
    f = open(name, "r")
    mylines = []
    with open('beamline EllKB.txt', 'rt') as myfile:
        for myline in myfile:
            mylines.append(myline)
    f.close()

    # -------------------------------------------------------------------------
    # OBTAIN GENERAL PARAMETERS: (obtains general parameters of the beamline)
    distances = []
    angles = []
    incangles = []
    leng = len(mylines)
    dimx = []
    dimy = []

    for linea in range(leng):
        mylines[linea] = mylines[linea].strip()
        if mylines[linea] == '#--1.1.Distances----------':
            distances.append(mylines[linea + 1].split()[2])
        if mylines[linea].find("Drift(") != -1:
            a = mylines[linea][mylines[linea].find('Drift(') + len('Drift('):].split()[0].strip(',').strip(')')
            distances.append(a)
        if mylines[linea] == '#--1.2.Angles-------------':
            for n in range(5):
                angles.append(mylines[linea + n + 2])
                angles[n] = angles[n].split()[1]
                angles[n] = angles[n].strip("=")
                angles[n] = str(float(angles[n]))
        if mylines[linea].find('theta=') != -1:
            incangles.append(mylines[linea])
        if mylines[linea].find("Dx") != -1:
            try:
                dimx.append(str(float(mylines[linea].split()[4].strip(',').strip('Dx='))))
                dimy.append(str(float(mylines[linea].split()[5].strip(')').strip('Dy='))))
            except:
                dimy.append(str(float(mylines[linea].split()[6].strip(')').strip('Dy='))))

    lastmirrortoscreen = distances[len(distances) - 1]
    distances = distances[0:len(distances) - 1]

    # This filter finds if the angle is the one selected and obtains non-repeated parameters:
    values = []
    for ii in range(len(incangles)):
        incangles[ii] = incangles[ii].strip(",")
        incangles[ii] = incangles[ii].split('=')[1]
        for linea in range(leng):
            if mylines[linea].find(incangles[ii] + '=') != -1:
                values.append(mylines[linea])
    values = list(set(values))

    valueangles = np.zeros((len(values), 3), dtype=object)
    for k in range(len(values)):
        values[k] = values[k].split()
        values[k][0] = values[k][0].strip("=")
        values[k][2] = values[k][2].strip("#")
        valueangles[k, 0] = str(values[k][0])
        valueangles[k, 1] = values[k][1]
        valueangles[k, 2] = values[k][2]
        if valueangles[k][2] == '[rad]':
            valueangles[k, 1] = math.radians(float(valueangles[k, 1]))
            valueangles[k, 2] = '[deg]'

    # Assigns a value of theta for each mirror:
    for j in range(len(incangles)):
        for u in range(len(valueangles)):
            if incangles[j] == valueangles[u][0]:
                incangles[j] = valueangles[u][1]

    # -------------------------------------------------------------------------
    # ANALYSE TYPE OF OPTICAL ELEMENTS:
    Material = [''] * numirr
    Shapes = ['c'] * numirr
    typo = []

    for ii in range(numirr):
        if matr[0, ii] == 'M':
            typo.append('Mirror' + str(ii))
            for linea in range(40, leng):
                if mylines[linea].find('mirror') != -1:
                    Material[ii] = matr[1, ii]
        if matr[0, ii] == 'A':
            typo.append('Aperture')
            for linea in range(0, leng):
                if mylines[linea] == '#Aperture -------------------------------------------------------------------':
                    Material[ii] = matr[1, ii]
                    if mylines[linea + 1].find("shape='c'") != -1:
                        if mylines[linea + 1].find("Dx") != -1:
                            Shapes[ii] = 'c'
                            incangles.insert(ii, math.pi / 2)

    for j in range(numirr):
        if dimx[j] != dimy[j]:
            Shapes[j] = 'e'

    dimy = dimy[0:numirr]
    dimx = dimx[0:numirr]
    distances = distances[0:numirr]
    incangles = incangles[0:numirr]

    # CREATE DATAFRAME WITH INFO
    d = {
        'Material': Material,
        'Incangles': incangles,
        'X Dimention': dimx,
        'Y Dimention': dimy,
        'Distances': distances,
        'Shape': Shapes
    }
    Information = pd.DataFrame(data=d, index=typo)

    # -------------------------------------------------------------------------
    # DIFFRACTION EFFICIENCY
    # Sum distances so that there is the total value from source to mirror:
    for l in range(1, Information.shape[0]):
        Information['Distances'][l] = float(Information['Distances'][l]) + float(Information['Distances'][l - 1])

    # Create vector with the diffraction efficiencies:
    DiffEff = []
    for k in range(Information.shape[0]):
        Beam = float(Information['Distances'][k]) * math.tan(float(Divergence) / 2 * 1e-6)
        Proj = abs(math.sin(float(Information['Incangles'][k]))) * Beam
        if Information['Shape'][k] == 'c':
            if Proj / float(Information['X Dimention'][k]) * 2 > 1:
                DiffEff.append((float(Information['X Dimention'][k]) / 2 / Proj) ** 2)
            elif Proj / float(Information['X Dimention'][k]) / 2 <= 1:
                DiffEff.append(1)
        elif Information['Shape'][k] == 'e':
            if Proj / float(Information['Y Dimention'][k]) * 2 > 1:
                DiffEff.append(float(Information['X Dimention'][k]) * float(Information['Y Dimention'][k]) / 2 / Proj ** 2)
            elif Proj / float(Information['X Dimention'][k]) / 2 <= 1:
                DiffEff.append(1)

    # Obtains from the web the different Reflectivities:
    Ref = pd.DataFrame()
    for w in range(Information.shape[0]):
        if Information.index[w] == 'Aperture':
            ref = [1] * (int(lambdanum) + 1)
        elif Information.index[w] != 'Aperture':
            if Information['Material'][w] == 'N':
                material = 'Ni'
            elif Information['Material'][w] == 'P':
                material = 'Pt'
            elif Information['Material'][w] == 'C':
                material = 'C'
            else:
                print('Error: Lacking material of mirror ' + str(w))
                continue
            ref, wave = thickmirror2(lambdamin, lambdamax, lambdanum, pol, density, material, roughness,
                                     angle=str(Information['Incangles'][w]))
        Ref['Mirror' + str(w + 1)] = pd.Series(ref)

    # Only in order to create the titles for the columns:
    vec = list(Ref.columns)
    for i in range(Ref.shape[1] - 1):
        if Information.index[i] == 'Aperture':
            vec[i] = 'Aperture'
            for a in range(i, len(vec) - 1):
                vec[a + 1] = 'Mirror' + str(a + 1)
    Ref.columns = vec
    Ref.index = wave
    vec.append('Total Efficiency')

    # Create DataFrame that accumulates the diff. eff. for each lambda:
    Effofeachmirror = pd.DataFrame()
    for l in range(Ref.shape[1]):
        di = []
        for o in range(Ref.shape[0]):
            di.append(float(Ref.iloc[o, l]) * float(DiffEff[l]))
        Effofeachmirror['Mirror' + str(l + 1)] = pd.Series(di)

    total = []
    for q in range(Ref.shape[0]):
        total.append(Effofeachmirror.iloc[q, :].prod())

    Effofeachmirror['Total Eff'] = pd.Series(total)
    Effofeachmirror.columns = vec
    Effofeachmirror.index = wave

    # Select the lambda:
    for p in range(Effofeachmirror.shape[0]):
        if float(wavelen) == float(Effofeachmirror.index[p]):
            Reflectivity = list(Effofeachmirror.iloc[p])
            break
        elif float(wavelen) > float(Effofeachmirror.index[p]) and float(wavelen) < float(Effofeachmirror.index[p + 1]):
            Reflectivity = (Effofeachmirror.iloc[p] + Effofeachmirror.iloc[p]) / 2
            break

    return Reflectivity, Effofeachmirror