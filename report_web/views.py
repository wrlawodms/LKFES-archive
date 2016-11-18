#-*-coding:utf-8-*-
from django.shortcuts import render, get_object_or_404, Http404
from django.http import HttpResponse
from .models import Post
from lkfes_server import settings
import errno
import os
import json
import math
from django.views.decorators.csrf import csrf_exempt
import difflib
# Create your views here.

def list(request, page=1):
	length = 10
	page = int(page)
	latest_posts = Post.objects.order_by('-pub_date')[(page-1)*length:(page-1)*length+length]
	posts_cnt = len(Post.objects.all())
	# latest_posts = Post.objects.order_by('-pub_date')
	context = {'latest_posts' : latest_posts,
			   'cnt_pages' : range(1, int(math.ceil(posts_cnt/float(length)))+1)
			   }
	return render(request, 'report_list.html', context)

def report(request, post_id):
	post_id = int(post_id)
	post = get_object_or_404(Post, pk=post_id)
	post_files_dir = settings.MEDIA_ROOT+str(post.pk)
	#hard protocol!
	with open(post_files_dir+'/before.log.sw_spec') as f:
		post.before_sw_spec = json.load(f)
	with open(post_files_dir + '/after.log.sw_spec') as f:
		post.after_sw_spec = json.load(f)
	with open(post_files_dir + '/hw_spec') as f:
		post.hw_spec = json.load(f)
	with open(post_files_dir + '/before.log') as f:
		post.before_log = f.read()
	with open(post_files_dir + '/after.log') as f:
		post.after_log = f.read()
	post.files = os.listdir(post_files_dir)
	post.diffs = []
	for l in difflib.ndiff(post.before_log.splitlines(), post.after_log.splitlines()):
		if not l.startswith('?'):
			post.diffs.append(l)
	# for res in post.hw_spec:
	context = {'post' : post}
	return render(request, 'report_deatil.html', context)

@csrf_exempt
def post(request):
	if request.method == 'POST':  # upload
		title = request.POST['title']
		desc = request.POST['desc']
		reporter = request.POST['reporter']
		files = request.FILES.values()
		#have to confirm to server file protocol
		f_names = [f.name for f in files]
		print(f_names)
		if not sorted(f_names) == \
			sorted(['before.log', 'after.log', 'before.log.sw_spec', 'after.log.sw_spec', 'hw_spec', 'extra.zip']):
			return HttpResponse(status=400)
		post = Post(title=title, desc=desc, reporter=reporter)
		post.save()#TODO consistency problem
		for f in files:
			upload_file(f, "wb", file_path=settings.MEDIA_ROOT + str(post.pk) + '/' + f.name)
		return HttpResponse('OK')

def download(request, post_id, file_name):
	response = HttpResponse()
	response['mimetype'] = "application/octet-stream"
	response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
	file_path = settings.MEDIA_ROOT+str(post_id)+'/'+file_name
	print "request download " + file_path
	if not os.path.isfile(file_path):
		raise Http404("There is no such file.")
	with open(file_path, 'rb') as file:
		response.write(file.read())
	return response



def upload_file(file, mode, file_path=None, root=settings.MEDIA_ROOT):
	if not file_path:
		file_path = root+file.name
	print 'upload_file is called , path : '+file_path
	try:
		os.makedirs(os.path.dirname(file_path))
	except OSError as exc:  # Guard against race condition
		if exc.errno != errno.EEXIST:
			pass
	with open(file_path, mode) as destination:
		for chunk in file.chunks():
			destination.write(chunk)


'''
TODO :
파일 업로드(정적데이터
업로드 된 파일 다운로드할 수 있게
업로드 된 파일 중 로그들 보여주기
업로드 된 파일 중 로그들의 diff보여주기
디자인 정리
'''
