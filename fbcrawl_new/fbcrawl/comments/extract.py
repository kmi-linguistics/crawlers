import os 
import csv

working_dir = os.getcwd()

post_dir = working_dir[:working_dir.rfind('/')] + '/posts'

allUrls = {}
text_url = {}
post_id = {}
spoint = 0
bpoint = 0
print ('Post Dir', post_dir)
for cur_dir_path, subdirs, files in os.walk(post_dir):
    for curnt_file in files:
        file_path = cur_dir_path + os.sep + curnt_file
        if file_path.endswith ('.csv') and curnt_file != 'all_comments.csv':
            cur_coms = 0
            cur_post = 0

            with open (file_path, 'r') as f:
                print ('Processing', curnt_file)
                reader = csv.reader(f)
                for row in reader:
                    if row[12] != 'post_id':
                        url = row[12]
                        pName = curnt_file.replace ('.csv', '')
                        allUrls[url] = pName
                        text_url[url] = row[3]
                        post_id[pName+'_'+url] = ['Post' + '#_#' + row[3]]


with open ('all_comments.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[6] != 'url':
            full_url = row[6]
            #print ('Full URL', full_url)
            if 'replies/?ctoken=' in full_url:                
                spoint = len ('https://mbasic.facebook.com/comment/replies/?ctoken=')
                bpoint = full_url.find('_')
            elif 'story.php?story_fbid=' in full_url:
                spoint = len ('https://mbasic.facebook.com/story.php?story_fbid=')
                bpoint = full_url.find('&id=')
            
            fbid = full_url[spoint:bpoint]
            cid = full_url[bpoint+1:full_url.find ('&')].strip()
            #print ('FB ID', fbid)
            #print ('Comment ID', cid)
            if fbid in allUrls:
                fname = allUrls[fbid]
                map_key = fname+'_'+fbid

                if map_key in post_id:
                    post_id [map_key].append (cid+'#_#'+row[4])
                else:
                    print ('Map key not found', map_key)


fname = ''
prev_fid = ''
print ('Total URLs', len (allUrls))



with open ('comments_posts.csv', 'w') as f_w, open ('only_comments.csv', 'w') as f_w2:
    print ('Adding all comments crawled')
    writer = csv.writer(f_w)
    writer2 = csv.writer(f_w2)
    writer.writerow(['Page', 'Post ID', 'Comment ID', 'Comment/Post'])
    writer2.writerow(['Page', 'Post ID', 'Comment ID', 'Comment'])

    for map_key in post_id:
        map_key_l = map_key.split('_')
        first = True
        all_coms = post_id[map_key]
        for com_id in all_coms:
            com_id_l = com_id.split('#_#')
            if first:                    
                writer.writerow([map_key_l[0], map_key_l[1], com_id_l[0], com_id_l[1]])
                first = False
            else:
                writer.writerow([map_key_l[0], map_key_l[1], com_id_l[0], com_id_l[1]])
                writer2.writerow([map_key_l[0], map_key_l[1], com_id_l[0], com_id_l[1]])
        



                
