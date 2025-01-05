from pathlib import Path

import yaml
from flask import Flask, flash, redirect, render_template, request, url_for

from utils.constants import SECRETS_YAML, WORK_PREFERENCES_YAML

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            config = {
                'remote': request.form.get('remote') == 'true',
                'experience_level': {
                    'internship': request.form.get('internship') == 'on',
                    'entry': request.form.get('entry') == 'on',
                    'associate': request.form.get('associate') == 'on',
                    'mid_senior_level': request.form.get('mid_senior_level') == 'on',
                    'director': request.form.get('director') == 'on',
                    'executive': request.form.get('executive') == 'on'
                },
                'job_types': {
                    'full_time': request.form.get('full_time') == 'on',
                    'contract': request.form.get('contract') == 'on',
                    'part_time': request.form.get('part_time') == 'on',
                    'temporary': request.form.get('temporary') == 'on',
                    'internship': request.form.get('job_internship') == 'on',
                    'other': request.form.get('other') == 'on',
                    'volunteer': request.form.get('volunteer') == 'on'
                },
                'date': {
                    'all_time': request.form.get('date_filter') == 'all_time',
                    'month': request.form.get('date_filter') == 'month',
                    'week': request.form.get('date_filter') == 'week',
                    '24_hours': request.form.get('date_filter') == '24_hours'
                },
                'positions': request.form.get('positions').split(','),
                'locations': request.form.get('locations').split(','),
                'location_blacklist': request.form.get('location_blacklist').split(',') if request.form.get('location_blacklist') else [],
                'distance': int(request.form.get('distance')),
                'company_blacklist': request.form.get('company_blacklist').split(',') if request.form.get('company_blacklist') else [],
                'title_blacklist': request.form.get('title_blacklist').split(',') if request.form.get('title_blacklist') else []
            }
            
            # Save to YAML file
            with open(WORK_PREFERENCES_YAML, 'w') as f:
                yaml.dump(config, f)
                
            # Save secrets separately
            secrets = {
                'email': request.form.get('email'),
                'openai_api_key': request.form.get('openai_api_key')
            }
            with open(SECRETS_YAML, 'w') as f:
                yaml.dump(secrets, f)
                
            flash('Configuration saved successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error saving configuration: {str(e)}', 'error')
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 