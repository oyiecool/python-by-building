scores = np.array([[78, 85, 92], [88, 79, 95], [65, 70, 72]])   # students x exams
scores.mean()            # overall average
scores.mean(axis=0)      # average per exam
scores.max(axis=1)       # best score per student
scores.argmax(axis=1)    # which exam was each student's best
np.percentile(scores, 90)
np.corrcoef(scores[:, 0], scores[:, 2])[0, 1]   # do exam 1 and exam 3 agree?
