#### MySQL queries ####

def get_treated_subclass_query(year, category, baseline=True):
    flag_names = {
        'diabetes': 'sp_diabetes_flag',
        'cardio': 'cardiovascular',
        'dementia': 'dementia_flag'
    }
    table = 'annual_matched_profile_flags' if baseline==True else 'annual_simulated_treatment_flags'
    treated_subclass_query = f"""
        SELECT 
            mp.subclass,
            mp.treated,
            mp.profile_id as profile_id_t, 
            ampf.{flag_names[category]} as {flag_names[category] + '_t'}
        FROM hbs.matched_profiles mp
        LEFT JOIN hbs.{table} ampf
            ON mp.profile_id = ampf.profile_id
            AND ampf.`year`={year}
        WHERE mp.treated = 1 
            AND ampf.death_flag < 2
        ;"""
    return treated_subclass_query


def get_control_subclass_query(year, category):
    # select one of each control subclass alive in year
    # set seed parameter n of RAND(n) in query to ensure consistent response
    flag_names = {
        'diabetes': 'sp_diabetes_flag',
        'cardio': 'cardiovascular',
        'dementia': 'dementia_flag'
    }
    control_subclass_query = f"""
        select t1.subclass, t1.treated, t1.profile_id as profile_id_c, t1.{flag_names[category]} as {flag_names[category] + '_c'} 
        from (
            select 
                mp.profile_id, 
                mp.treated,
                mp.subclass, 
                ampf.{flag_names[category]},
                row_number() over (partition by mp.subclass order by rand(52)) as rownum 
            from hbs.matched_profiles mp
            left join hbs.annual_matched_profile_flags ampf
                on mp.profile_id = ampf.profile_id
                and ampf.`year`={year}
            where mp.treated = 0 
                and ampf.death_flag < 2
            ) t1
        where t1.rownum=1
        order by t1.subclass
        ;"""
    return control_subclass_query

